from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.account import Account
from app.models.asset import Asset
from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionItem


router = APIRouter()


def _to_item(item: Transaction) -> TransactionItem:
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


@router.get("", response_model=list[TransactionItem])
def list_transactions(db: Session = Depends(get_db)) -> list[TransactionItem]:
    items = db.scalars(select(Transaction).order_by(Transaction.created_at.desc(), Transaction.id.desc())).all()
    return [_to_item(item) for item in items]


@router.post("", response_model=TransactionItem, status_code=status.HTTP_201_CREATED)
def create_transaction(payload: TransactionCreate, db: Session = Depends(get_db)) -> TransactionItem:
    account = db.scalar(select(Account).where(Account.id == payload.account_id))
    if account is None:
        raise HTTPException(status_code=404, detail="Account not found")

    asset = None
    if payload.asset_id is not None:
        asset = db.scalar(select(Asset).where(Asset.id == payload.asset_id))
    elif payload.asset_code:
        asset = db.scalar(select(Asset).where(Asset.code == payload.asset_code))
        if asset is None:
            if not payload.asset_name or not payload.asset_type or not payload.market:
                raise HTTPException(status_code=400, detail="Missing asset metadata")
            asset = Asset(
                code=payload.asset_code,
                name=payload.asset_name,
                asset_type=payload.asset_type,
                market=payload.market,
                currency=payload.currency,
                target_weight=payload.target_weight,
            )
            db.add(asset)
            db.flush()

    if asset is None:
        raise HTTPException(status_code=404, detail="Asset not found")

    item = Transaction(
        asset_id=asset.id,
        account_id=payload.account_id,
        action=payload.action,
        quantity=payload.quantity,
        price=payload.price,
        amount=payload.amount,
        fee=payload.fee,
        applied_date=payload.applied_date,
        confirmed_date=payload.confirmed_date,
        nav_date=payload.nav_date,
        status=payload.status,
        note=payload.note,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return _to_item(item)
