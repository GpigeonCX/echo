from datetime import datetime

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class PriceSnapshot(Base):
    __tablename__ = "price_snapshot"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("asset.id"), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(18, 6), nullable=False)
    fx_rate_to_cny: Mapped[float] = mapped_column(Numeric(18, 6), default=1, nullable=False)
    captured_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
