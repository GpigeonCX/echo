from datetime import date, datetime

from pydantic import BaseModel, Field


class TransactionBase(BaseModel):
    asset_id: int | None = None
    asset_code: str | None = None
    asset_name: str | None = None
    asset_type: str | None = None
    market: str | None = None
    currency: str = "CNY"
    target_weight: float = 0
    account_id: int
    action: str
    quantity: float = Field(ge=0)
    price: float = Field(ge=0)
    amount: float = Field(ge=0)
    fee: float = Field(ge=0, default=0)
    applied_date: date
    confirmed_date: date | None = None
    nav_date: date | None = None
    status: str = "confirmed"
    note: str | None = None


class TransactionCreate(TransactionBase):
    pass


class TransactionItem(BaseModel):
    id: int
    asset_id: int
    account_id: int
    action: str
    quantity: float
    price: float
    amount: float
    fee: float
    applied_date: date
    confirmed_date: date | None = None
    nav_date: date | None = None
    status: str
    note: str | None = None
    created_at: datetime
