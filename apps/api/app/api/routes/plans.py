from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.investment_plan import InvestmentPlan
from app.schemas.plan import PlanSummary, PlanUpdate
from app.services.portfolio import list_plan_summary


router = APIRouter()


@router.get("", response_model=list[PlanSummary])
def list_plans(db: Session = Depends(get_db)) -> list[PlanSummary]:
    return list_plan_summary(db)


@router.put("/{plan_id}", response_model=PlanSummary)
def update_plan(plan_id: int, payload: PlanUpdate, db: Session = Depends(get_db)) -> PlanSummary:
    plan = db.scalar(select(InvestmentPlan).where(InvestmentPlan.id == plan_id))
    if plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")

    plan.name = payload.name
    plan.total_budget = payload.total_budget
    plan.months = payload.months
    plan.first_month_ratio = payload.first_month_ratio
    plan.status = payload.status
    db.add(plan)
    db.commit()

    summary = list_plan_summary(db)
    matched = next((item for item in summary if item.id == plan_id), None)
    if matched is None:
      raise HTTPException(status_code=500, detail="Plan summary not found")
    return matched
