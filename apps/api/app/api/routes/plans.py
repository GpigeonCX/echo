from fastapi import APIRouter

from app.schemas.plan import PlanSummary


router = APIRouter()


@router.get("", response_model=list[PlanSummary])
def list_plans() -> list[PlanSummary]:
    return [
        PlanSummary(
            name="2026Q2 建仓计划",
            total_budget=500000,
            months=6,
            first_month_ratio=0.4,
            status="in_progress",
            planned_this_month=52800,
            invested_this_month=20000,
        )
    ]
