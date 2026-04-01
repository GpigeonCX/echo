from collections import defaultdict
from decimal import Decimal

from sqlalchemy import desc, select
from sqlalchemy.orm import Session

from app.models.asset import Asset
from app.models.investment_plan import InvestmentPlan
from app.models.price_snapshot import PriceSnapshot
from app.models.transaction import Transaction
from app.schemas.asset import HoldingSummaryItem
from app.schemas.dashboard import AllocationItem, DashboardSummary
from app.schemas.plan import PlanSummary
def list_holdings_summary(db: Session) -> list[HoldingSummaryItem]:
    assets = db.scalars(select(Asset).order_by(Asset.code)).all()
    confirmed_transactions = db.scalars(
        select(Transaction).where(Transaction.status == "confirmed").order_by(Transaction.created_at)
    ).all()
    snapshot_rows = db.scalars(
        select(PriceSnapshot).order_by(PriceSnapshot.asset_id, desc(PriceSnapshot.captured_at))
    ).all()
    latest_snapshots: dict[int, PriceSnapshot] = {}
    for item in snapshot_rows:
        latest_snapshots.setdefault(item.asset_id, item)

    totals: dict[int, dict[str, Decimal]] = defaultdict(lambda: {"quantity": Decimal("0"), "amount": Decimal("0"), "fee": Decimal("0")})
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
        quantity = totals[asset.id]["quantity"]
        invested_amount = totals[asset.id]["amount"]
        fee = totals[asset.id]["fee"]
        if quantity <= 0 and invested_amount == 0:
            continue

        snapshot = latest_snapshots.get(asset.id)
        price = Decimal(snapshot.price) if snapshot else Decimal("1")
        fx_rate = Decimal(snapshot.fx_rate_to_cny) if snapshot else Decimal("1")
        market_value = quantity * price * fx_rate
        cost = invested_amount + fee
        avg_cost = (cost / quantity) if quantity > 0 else Decimal("0")
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
    peak_assets = max(total_assets, 336000)
    drawdown_rate = ((total_assets - peak_assets) / peak_assets) if peak_assets else 0

    allocation_map: dict[str, float] = {"基金": 0.0, "港股": 0.0, "现金": 0.0}
    alerts: list[str] = []
    for item in holdings:
        if item.asset_type == "hk_stock":
            allocation_map["港股"] += item.market_value_cny
        elif item.asset_type in {"cash", "money_fund"}:
            allocation_map["现金"] += item.market_value_cny
        else:
            allocation_map["基金"] += item.market_value_cny

        deviation = item.current_weight - item.target_weight
        if abs(deviation) >= 0.05:
            alerts.append(f"{item.name} 偏离目标权重 {deviation * 100:.2f}%")

    if drawdown_rate <= -0.15:
        alerts.insert(0, f"组合回撤 {drawdown_rate * 100:.2f}%，已触发弹药提醒")
    else:
        alerts.insert(0, f"组合回撤 {drawdown_rate * 100:.2f}%，暂未触发弹药阈值")

    return DashboardSummary(
        total_assets=total_assets,
        cash_assets=cash_assets,
        unrealized_pnl=unrealized_pnl,
        drawdown_rate=drawdown_rate,
        peak_assets=peak_assets,
        allocation=[AllocationItem(name=name, value=value) for name, value in allocation_map.items() if value > 0],
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
        planned_this_month = float(plan.total_budget) * (float(plan.first_month_ratio) if plan.status == "in_progress" else 0)
        summaries.append(
            PlanSummary(
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
