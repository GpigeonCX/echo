from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.account import Account
from app.models.asset import Asset
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionItem


router = APIRouter()


@router.get("", response_model=list[TransactionItem])
def list_transactions(db: Session = Depends(get_db)) -> list[TransactionItem]:
    items = db.scalars(select(Transaction).order_by(Transaction.created_at.desc(), Transaction.id.desc())).all()
    return [
        TransactionItem(
            id=item.id,
            asset_id=item.asset_id,
            account_id=item.account_id,
            action=item.action,
            quantity=float(item.quantity),
            price=float(item.price),
            amount=float(item.amount),
            fee=float(item.fee),
            applied_date=item.applied_date,
            confirmed_date=item.confirmed_date,
            nav_date=item.nav_date,
            status=item.status,
            note=item.note,
            created_at=item.created_at,
        )
        for item in items
    ]


@router.post("", response_model=TransactionItem, status_code=status.HTTP_201_CREATED)
def create_transaction(payload: TransactionCreate, db: Session = Depends(get_db)) -> TransactionItem:
    asset = db.scalar(select(Asset).where(Asset.id == payload.asset_id))
    account = db.scalar(select(Account).where(Account.id == payload.account_id))
    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")

    item = Transaction(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return TransactionItem(
        id=item.id,
        asset_id=item.asset_id,
        account_id=item.account_id,
        action=item.action,
        quantity=float(item.quantity),
        price=float(item.price),
        amount=float(item.amount),
        fee=float(item.fee),
        applied_date=item.applied_date,
        confirmed_date=item.confirmed_date,
        nav_date=item.nav_date,
        status=item.status,
        note=item.note,
        created_at=item.created_at,
    )
