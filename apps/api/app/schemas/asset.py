from pydantic import BaseModel


class AssetItem(BaseModel):
    id: int | None = None
    code: str
    name: str
    asset_type: str
    market: str
    currency: str
    target_weight: float


class HoldingSummaryItem(AssetItem):
    quantity: float
    current_price: float
    average_cost: float
    market_value_cny: float
    profit_cny: float
    current_weight: float
