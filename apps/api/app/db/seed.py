from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.asset import Asset
from app.models.investment_plan import InvestmentPlan
from app.models.price_snapshot import PriceSnapshot
from app.models.transaction import Transaction


def seed_demo_data(db: Session) -> None:
    has_asset = db.scalar(select(Asset.id).limit(1))
    if has_asset:
        return

    account = Account(name="默认账户", account_type="virtual", currency="CNY")
    db.add(account)
    db.flush()

    assets = [
        Asset(code="000588", name="货币基金", asset_type="cash", market="CASH", currency="CNY", target_weight=Decimal("0.12")),
        Asset(code="161125", name="标普500", asset_type="fund", market="CN_FUND", currency="CNY", target_weight=Decimal("0.32")),
        Asset(code="270042", name="纳指100", asset_type="fund", market="CN_FUND", currency="CNY", target_weight=Decimal("0.10")),
        Asset(code="00700", name="腾讯控股", asset_type="hk_stock", market="HK", currency="HKD", target_weight=Decimal("0.08")),
    ]
    db.add_all(assets)
    db.flush()

    latest_day = date(2026, 4, 1)
    snapshots = [
        PriceSnapshot(asset_id=assets[0].id, price=Decimal("1.000000"), fx_rate_to_cny=Decimal("1.000000"), captured_at=datetime(2026, 4, 1, 10, 0, 0)),
        PriceSnapshot(asset_id=assets[1].id, price=Decimal("1.245000"), fx_rate_to_cny=Decimal("1.000000"), captured_at=datetime(2026, 4, 1, 15, 0, 0)),
        PriceSnapshot(asset_id=assets[2].id, price=Decimal("1.980000"), fx_rate_to_cny=Decimal("1.000000"), captured_at=datetime(2026, 4, 1, 15, 0, 0)),
        PriceSnapshot(asset_id=assets[3].id, price=Decimal("320.400000"), fx_rate_to_cny=Decimal("0.920000"), captured_at=datetime(2026, 4, 1, 15, 0, 0)),
    ]
    db.add_all(snapshots)

    transactions = [
        Transaction(
            asset_id=assets[0].id,
            account_id=account.id,
            action="deposit",
            quantity=Decimal("60000"),
            price=Decimal("1"),
            amount=Decimal("60000"),
            fee=Decimal("0"),
            applied_date=latest_day,
            status="confirmed",
            note="弹药仓初始资金",
        ),
        Transaction(
            asset_id=assets[1].id,
            account_id=account.id,
            action="buy",
            quantity=Decimal("128000"),
            price=Decimal("1.200000"),
            amount=Decimal("153600"),
            fee=Decimal("0"),
            applied_date=date(2026, 3, 20),
            confirmed_date=date(2026, 3, 21),
            nav_date=date(2026, 3, 21),
            status="confirmed",
        ),
        Transaction(
            asset_id=assets[2].id,
            account_id=account.id,
            action="buy",
            quantity=Decimal("18000"),
            price=Decimal("1.850000"),
            amount=Decimal("33300"),
            fee=Decimal("0"),
            applied_date=date(2026, 3, 12),
            confirmed_date=date(2026, 3, 13),
            nav_date=date(2026, 3, 13),
            status="confirmed",
        ),
        Transaction(
            asset_id=assets[3].id,
            account_id=account.id,
            action="buy",
            quantity=Decimal("100"),
            price=Decimal("310.000000"),
            amount=Decimal("28520"),
            fee=Decimal("100"),
            applied_date=date(2026, 3, 15),
            status="confirmed",
        ),
    ]
    db.add_all(transactions)
    db.add(
        InvestmentPlan(
            name="2026Q2 建仓计划",
            total_budget=Decimal("500000"),
            months=6,
            first_month_ratio=Decimal("0.4"),
            status="in_progress",
        )
    )
    db.commit()
