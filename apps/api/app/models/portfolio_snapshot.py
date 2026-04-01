from datetime import datetime

from sqlalchemy import Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class PortfolioSnapshot(Base):
    __tablename__ = "portfolio_snapshot"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    total_assets: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    peak_assets: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    drawdown_rate: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    recorded_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, nullable=False)
