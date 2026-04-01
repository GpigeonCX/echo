from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.asset import Asset
from app.services.portfolio import list_holdings_summary
from app.schemas.asset import AssetItem
from app.schemas.asset import HoldingSummaryItem


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


@router.get("/holdings", response_model=list[HoldingSummaryItem])
def get_holdings(db: Session = Depends(get_db)) -> list[HoldingSummaryItem]:
    return list_holdings_summary(db)
