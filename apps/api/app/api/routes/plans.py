from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.services.portfolio import list_plan_summary
from app.schemas.plan import PlanSummary


router = APIRouter()


@router.get("", response_model=list[PlanSummary])
def list_plans(db: Session = Depends(get_db)) -> list[PlanSummary]:
    return list_plan_summary(db)
