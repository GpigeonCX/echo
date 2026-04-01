from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.schemas.quote import QuoteSyncResult
from app.services.quotes import sync_quotes_once


router = APIRouter()


@router.post("/sync", response_model=QuoteSyncResult)
def sync_quotes(db: Session = Depends(get_db)) -> QuoteSyncResult:
    return sync_quotes_once(db)
