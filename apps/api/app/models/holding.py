from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Holding(Base):
    __tablename__ = "holding"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("asset.id"), nullable=False)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), nullable=False)
    quantity: Mapped[float] = mapped_column(Numeric(18, 6), default=0, nullable=False)
    average_cost: Mapped[float] = mapped_column(Numeric(18, 6), default=0, nullable=False)
    market_value_cny: Mapped[float] = mapped_column(Numeric(18, 2), default=0, nullable=False)
