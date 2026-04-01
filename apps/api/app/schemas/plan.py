from pydantic import BaseModel


class PlanSummary(BaseModel):
    name: str
    total_budget: float
    months: int
    first_month_ratio: float
    status: str
    planned_this_month: float
    invested_this_month: float
