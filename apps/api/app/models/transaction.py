from datetime import date, datetime

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Transaction(Base):
    __tablename__ = "transaction_record"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("asset.id"), nullable=False)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), nullable=False)
    action: Mapped[str] = mapped_column(
        Enum(
            "buy",
            "sell",
            "deposit",
            "withdraw",
            "dividend",
            "manual_adjustment",
            name="transaction_action_enum",
        ),
        nullable=False,
    )
    quantity: Mapped[float] = mapped_column(Numeric(18, 6), default=0, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(18, 6), default=0, nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(18, 2), default=0, nullable=False)
    fee: Mapped[float] = mapped_column(Numeric(18, 2), default=0, nullable=False)
    applied_date: Mapped[date] = mapped_column(Date, nullable=False)
    confirmed_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    nav_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[str] = mapped_column(
        Enum("pending", "confirmed", name="transaction_status_enum"),
        default="confirmed",
        nullable=False,
    )
    note: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
