from pydantic import BaseModel


class AssetItem(BaseModel):
    code: str
    name: str
    asset_type: str
    market: str
    currency: str
    target_weight: float
