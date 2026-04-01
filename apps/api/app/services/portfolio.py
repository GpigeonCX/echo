from collections import defaultdict
from decimal import Decimal

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.models.holding import Holding
from app.models.investment_plan import InvestmentPlan
from app.models.portfolio_snapshot import PortfolioSnapshot
from app.models.price_snapshot import PriceSnapshot
from app.models.transaction import Transaction
from app.schemas.asset import HoldingSummaryItem
from app.schemas.dashboard import AllocationItem, DashboardSummary, RebalanceSuggestionItem
from app.schemas.plan import PlanSummary


def _get_drawdown_stage(drawdown_rate: float) -> str:
    if drawdown_rate <= -0.35:
        return "third"
    if drawdown_rate <= -0.25:
        return "second"
    if drawdown_rate <= -0.15:
        return "first"
    return "none"


def _record_portfolio_snapshot(db: Session, total_assets: float, peak_assets: float, drawdown_rate: float) -> None:
    snapshot = PortfolioSnapshot(
        total_assets=total_assets,
        peak_assets=peak_assets,
        drawdown_rate=drawdown_rate,
    )
    db.add(snapshot)
    db.commit()


def list_holdings_summary(db: Session) -> list[HoldingSummaryItem]:
    assets = db.scalars(select(Asset).order_by(Asset.code)).all()
    manual_holdings = db.scalars(select(Holding)).all()
    confirmed_transactions = db.scalars(
        select(Transaction).where(Transaction.status == "confirmed").order_by(Transaction.created_at)
    ).all()
    snapshot_rows = db.scalars(
        select(PriceSnapshot).order_by(PriceSnapshot.asset_id, desc(PriceSnapshot.captured_at))
    ).all()
    latest_snapshots: dict[int, PriceSnapshot] = {}
    for item in snapshot_rows:
        latest_snapshots.setdefault(item.asset_id, item)
    manual_holding_map = {item.asset_id: item for item in manual_holdings}

    totals: dict[int, dict[str, Decimal]] = defaultdict(
        lambda: {"quantity": Decimal("0"), "amount": Decimal("0"), "fee": Decimal("0")}
    )
    for tx in confirmed_transactions:
        if tx.action in {"buy", "deposit"}:
            totals[tx.asset_id]["quantity"] += Decimal(tx.quantity)
            totals[tx.asset_id]["amount"] += Decimal(tx.amount)
            totals[tx.asset_id]["fee"] += Decimal(tx.fee)
        elif tx.action in {"sell", "withdraw"}:
            totals[tx.asset_id]["quantity"] -= Decimal(tx.quantity)
            totals[tx.asset_id]["amount"] -= Decimal(tx.amount)
            totals[tx.asset_id]["fee"] += Decimal(tx.fee)

    result: list[HoldingSummaryItem] = []
    total_market_value = Decimal("0")
    partials: list[dict[str, Decimal | str]] = []
    for asset in assets:
        manual_holding = manual_holding_map.get(asset.id)
        quantity = Decimal(manual_holding.quantity) if manual_holding else totals[asset.id]["quantity"]
        fee = totals[asset.id]["fee"]
        invested_amount = (
            Decimal(manual_holding.average_cost) * quantity
            if manual_holding
            else totals[asset.id]["amount"]
        )
        if quantity <= 0 and invested_amount == 0 and manual_holding is None:
            continue

        snapshot = latest_snapshots.get(asset.id)
        price = Decimal(snapshot.price) if snapshot else Decimal("1")
        fx_rate = Decimal(snapshot.fx_rate_to_cny) if snapshot else Decimal("1")
        market_value = quantity * price * fx_rate
        cost = invested_amount + fee
        avg_cost = Decimal(manual_holding.average_cost) if manual_holding else ((cost / quantity) if quantity > 0 else Decimal("0"))
        pnl = market_value - cost
        total_market_value += market_value
        partials.append(
            {
                "code": asset.code,
                "name": asset.name,
                "asset_type": asset.asset_type,
                "market": asset.market,
                "currency": asset.currency,
                "target_weight": Decimal(asset.target_weight),
                "quantity": quantity,
                "current_price": price,
                "average_cost": avg_cost,
                "market_value_cny": market_value,
                "profit_cny": pnl,
            }
        )

    for item in partials:
        weight = (item["market_value_cny"] / total_market_value) if total_market_value > 0 else Decimal("0")
        result.append(
            HoldingSummaryItem(
                code=str(item["code"]),
                name=str(item["name"]),
                asset_type=str(item["asset_type"]),
                market=str(item["market"]),
                currency=str(item["currency"]),
                target_weight=float(item["target_weight"]),
                current_weight=float(weight),
                quantity=float(item["quantity"]),
                current_price=float(item["current_price"]),
                average_cost=float(item["average_cost"]),
                market_value_cny=float(item["market_value_cny"]),
                profit_cny=float(item["profit_cny"]),
            )
        )
    return result


def get_dashboard_summary(db: Session) -> DashboardSummary:
    holdings = list_holdings_summary(db)
    total_assets = sum(item.market_value_cny for item in holdings)
    cash_assets = sum(item.market_value_cny for item in holdings if item.asset_type in {"cash", "money_fund"})
    unrealized_pnl = sum(item.profit_cny for item in holdings)
    existing_peak = db.scalar(
        select(PortfolioSnapshot.peak_assets).order_by(PortfolioSnapshot.peak_assets.desc()).limit(1)
    )
    peak_assets = max(total_assets, float(existing_peak or 0), 336000)
    drawdown_rate = ((total_assets - peak_assets) / peak_assets) if peak_assets else 0
    existing_max_drawdown = db.scalar(
        select(PortfolioSnapshot.drawdown_rate).order_by(PortfolioSnapshot.drawdown_rate.asc()).limit(1)
    )
    max_drawdown_rate = min(drawdown_rate, float(existing_max_drawdown or 0))
    drawdown_stage = _get_drawdown_stage(drawdown_rate)
    _record_portfolio_snapshot(db, total_assets, peak_assets, drawdown_rate)

    allocation_map: dict[str, float] = {"基金": 0.0, "港股": 0.0, "现金": 0.0}
    alerts: list[str] = []
    rebalance_suggestions: list[RebalanceSuggestionItem] = []

    for item in holdings:
        if item.asset_type == "hk_stock":
            allocation_map["港股"] += item.market_value_cny
        elif item.asset_type in {"cash", "money_fund"}:
            allocation_map["现金"] += item.market_value_cny
        else:
            allocation_map["基金"] += item.market_value_cny

        deviation = item.current_weight - item.target_weight
        if abs(deviation) >= 0.05:
            suggested_amount = (item.target_weight - item.current_weight) * total_assets
            alerts.append(f"{item.name} 偏离目标权重 {deviation * 100:.2f}%")
            rebalance_suggestions.append(
                RebalanceSuggestionItem(
                    code=item.code,
                    name=item.name,
                    current_weight=item.current_weight,
                    target_weight=item.target_weight,
                    deviation=deviation,
                    suggested_amount_cny=suggested_amount,
                )
            )

    if drawdown_rate <= -0.15:
        stage_text = {
            "first": "已触发第一档弹药提醒",
            "second": "已触发第二档弹药提醒",
            "third": "已触发第三档弹药提醒",
        }.get(drawdown_stage, "已触发弹药提醒")
        alerts.insert(0, f"组合回撤 {drawdown_rate * 100:.2f}%，{stage_text}")
    else:
        alerts.insert(0, f"组合回撤 {drawdown_rate * 100:.2f}%，暂未触发弹药阈值")

    return DashboardSummary(
        total_assets=total_assets,
        cash_assets=cash_assets,
        unrealized_pnl=unrealized_pnl,
        drawdown_rate=drawdown_rate,
        peak_assets=peak_assets,
        max_drawdown_rate=max_drawdown_rate,
        drawdown_stage=drawdown_stage,
        allocation=[AllocationItem(name=name, value=value) for name, value in allocation_map.items() if value > 0],
        rebalance_suggestions=rebalance_suggestions,
        alerts=alerts,
    )


def list_plan_summary(db: Session) -> list[PlanSummary]:
    plans = db.scalars(select(InvestmentPlan).order_by(InvestmentPlan.id.desc())).all()
    buy_amount = sum(
        float(item.amount)
        for item in db.scalars(
            select(Transaction).where(Transaction.action == "buy", Transaction.status == "confirmed")
        ).all()
    )
    summaries: list[PlanSummary] = []
    for plan in plans:
        planned_this_month = float(plan.total_budget) * (
            float(plan.first_month_ratio) if plan.status == "in_progress" else 0
        )
        summaries.append(
            PlanSummary(
                id=plan.id,
                name=plan.name,
                total_budget=float(plan.total_budget),
                months=plan.months,
                first_month_ratio=float(plan.first_month_ratio),
                status=plan.status,
                planned_this_month=planned_this_month,
                invested_this_month=buy_amount,
            )
        )
    return summaries
