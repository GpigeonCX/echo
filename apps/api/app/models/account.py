from sqlalchemy import Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Account(Base):
    __tablename__ = "account"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    account_type: Mapped[str] = mapped_column(
        Enum("broker", "fund_platform", "bank", "virtual", name="account_type_enum"),
        nullable=False,
    )
    currency: Mapped[str] = mapped_column(String(10), default="CNY", nullable=False)
