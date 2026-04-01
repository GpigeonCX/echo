from pydantic import BaseModel, Field


class AssetItem(BaseModel):
    id: int | None = None
    code: str
    name: str
    asset_type: str
    market: str
    currency: str
    target_weight: float


class AssetCreate(BaseModel):
    code: str
    name: str
    asset_type: str
    market: str
    currency: str = "CNY"
    target_weight: float = 0
    current_price: float = 1
    fx_rate_to_cny: float = 1


class ManualHoldingUpsert(BaseModel):
    account_id: int = 1
    code: str
    name: str
    asset_type: str
    market: str
    currency: str = "CNY"
    target_weight: float = 0
    quantity: float = Field(ge=0)
    average_cost: float = Field(ge=0)
    current_price: float = Field(ge=0)
    fx_rate_to_cny: float = Field(default=1, gt=0)


class HoldingSummaryItem(AssetItem):
    quantity: float
    current_price: float
    average_cost: float
    market_value_cny: float
    profit_cny: float
    current_weight: float
