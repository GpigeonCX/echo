from pydantic import BaseModel


class AllocationItem(BaseModel):
    name: str
    value: float


class DashboardSummary(BaseModel):
    total_assets: float
    cash_assets: float
    unrealized_pnl: float
    drawdown_rate: float
    peak_assets: float
    allocation: list[AllocationItem]
    alerts: list[str]
