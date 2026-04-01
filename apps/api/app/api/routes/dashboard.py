from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.services.portfolio import get_dashboard_summary
from app.schemas.dashboard import DashboardSummary


router = APIRouter()


@router.get("/summary", response_model=DashboardSummary)
def read_dashboard_summary(db: Session = Depends(get_db)) -> DashboardSummary:
    return get_dashboard_summary(db)
