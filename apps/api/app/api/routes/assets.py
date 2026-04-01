from fastapi import APIRouter

from app.schemas.asset import AssetItem


router = APIRouter()


@router.get("", response_model=list[AssetItem])
def list_assets() -> list[AssetItem]:
    return [
        AssetItem(
            code="161125",
            name="标普500",
            asset_type="fund",
            market="CN_FUND",
            currency="CNY",
            target_weight=0.32,
        ),
        AssetItem(
            code="00700",
            name="腾讯控股",
            asset_type="hk_stock",
            market="HK",
            currency="HKD",
            target_weight=0.08,
        ),
    ]
