from pydantic import BaseModel


class AllocationItem(BaseModel):
    name: str
    value: float


class RebalanceSuggestionItem(BaseModel):
    code: str
    name: str
    current_weight: float
    target_weight: float
    deviation: float
    suggested_amount_cny: float


class DashboardSummary(BaseModel):
    total_assets: float
    cash_assets: float
    unrealized_pnl: float
    drawdown_rate: float
    peak_assets: float
    max_drawdown_rate: float
    drawdown_stage: str
    allocation: list[AllocationItem]
    rebalance_suggestions: list[RebalanceSuggestionItem]
    alerts: list[str]
