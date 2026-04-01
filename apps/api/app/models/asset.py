from sqlalchemy import Boolean, Enum, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Asset(Base):
    __tablename__ = "asset"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    asset_type: Mapped[str] = mapped_column(
        Enum("fund", "hk_stock", "cash", "money_fund", name="asset_type_enum"),
        nullable=False,
    )
    market: Mapped[str] = mapped_column(String(32), nullable=False)
    currency: Mapped[str] = mapped_column(String(10), nullable=False, default="CNY")
    target_weight: Mapped[float] = mapped_column(Numeric(10, 4), default=0, nullable=False)
    auto_quote_enabled: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
