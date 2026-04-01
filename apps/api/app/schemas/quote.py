from datetime import datetime

from pydantic import BaseModel


class QuoteSyncItem(BaseModel):
    code: str
    price: float
    fx_rate_to_cny: float
    source: str


class QuoteSyncResult(BaseModel):
    success: bool
    synced_count: int
    synced_at: datetime
    message: str
    items: list[QuoteSyncItem]
