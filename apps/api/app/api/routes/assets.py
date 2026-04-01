from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.asset import Asset
from app.models.holding import Holding
from app.models.price_snapshot import PriceSnapshot
from app.schemas.asset import AssetCreate, AssetItem, HoldingSummaryItem, ManualHoldingUpsert
from app.services.portfolio import list_holdings_summary


router = APIRouter()


@router.get("", response_model=list[AssetItem])
def list_assets(db: Session = Depends(get_db)) -> list[AssetItem]:
    assets = db.scalars(select(Asset).order_by(Asset.code)).all()
    return [
        AssetItem(
            id=asset.id,
            code=asset.code,
            name=asset.name,
            asset_type=asset.asset_type,
            market=asset.market,
            currency=asset.currency,
            target_weight=float(asset.target_weight),
        )
        for asset in assets
    ]


@router.post("", response_model=AssetItem)
def create_asset(payload: AssetCreate, db: Session = Depends(get_db)) -> AssetItem:
    existing = db.scalar(select(Asset).where(Asset.code == payload.code))
    if existing is None:
        existing = Asset(
            code=payload.code,
            name=payload.name,
            asset_type=payload.asset_type,
            market=payload.market,
            currency=payload.currency,
            target_weight=Decimal(str(payload.target_weight)),
        )
        db.add(existing)
        db.flush()
    else:
        existing.name = payload.name
        existing.asset_type = payload.asset_type
        existing.market = payload.market
        existing.currency = payload.currency
        existing.target_weight = Decimal(str(payload.target_weight))

    db.add(
        PriceSnapshot(
            asset_id=existing.id,
            price=Decimal(str(payload.current_price)),
            fx_rate_to_cny=Decimal(str(payload.fx_rate_to_cny)),
            captured_at=datetime.utcnow(),
        )
    )
    db.commit()
    db.refresh(existing)
    return AssetItem(
        id=existing.id,
        code=existing.code,
        name=existing.name,
        asset_type=existing.asset_type,
        market=existing.market,
        currency=existing.currency,
        target_weight=float(existing.target_weight),
    )


@router.post("/manual-holdings", response_model=HoldingSummaryItem)
def upsert_manual_holding(payload: ManualHoldingUpsert, db: Session = Depends(get_db)) -> HoldingSummaryItem:
    asset = db.scalar(select(Asset).where(Asset.code == payload.code))
    if asset is None:
        asset = Asset(
            code=payload.code,
            name=payload.name,
            asset_type=payload.asset_type,
            market=payload.market,
            currency=payload.currency,
            target_weight=Decimal(str(payload.target_weight)),
        )
        db.add(asset)
        db.flush()
    else:
        asset.name = payload.name
        asset.asset_type = payload.asset_type
        asset.market = payload.market
        asset.currency = payload.currency
        asset.target_weight = Decimal(str(payload.target_weight))

    holding = db.scalar(
        select(Holding).where(Holding.asset_id == asset.id, Holding.account_id == payload.account_id)
    )
    market_value_cny = Decimal(str(payload.quantity)) * Decimal(str(payload.current_price)) * Decimal(str(payload.fx_rate_to_cny))
    if holding is None:
        holding = Holding(
            asset_id=asset.id,
            account_id=payload.account_id,
            quantity=Decimal(str(payload.quantity)),
            average_cost=Decimal(str(payload.average_cost)),
            market_value_cny=market_value_cny,
        )
        db.add(holding)
    else:
        holding.quantity = Decimal(str(payload.quantity))
        holding.average_cost = Decimal(str(payload.average_cost))
        holding.market_value_cny = market_value_cny

    db.add(
        PriceSnapshot(
            asset_id=asset.id,
            price=Decimal(str(payload.current_price)),
            fx_rate_to_cny=Decimal(str(payload.fx_rate_to_cny)),
            captured_at=datetime.utcnow(),
        )
    )
    db.commit()

    summary = next(item for item in list_holdings_summary(db) if item.code == payload.code)
    return summary


@router.get("/holdings", response_model=list[HoldingSummaryItem])
def get_holdings(db: Session = Depends(get_db)) -> list[HoldingSummaryItem]:
    return list_holdings_summary(db)
