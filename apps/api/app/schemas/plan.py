from pydantic import BaseModel, Field


class PlanSummary(BaseModel):
    id: int | None = None
    name: str
    total_budget: float
    months: int
    first_month_ratio: float
    status: str
    planned_this_month: float
    invested_this_month: float


class PlanUpdate(BaseModel):
    name: str
    total_budget: float = Field(gt=0)
    months: int = Field(gt=0)
    first_month_ratio: float = Field(ge=0, le=1)
    status: str
