from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TargetRule(Base):
    __tablename__ = "target_rule"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    version_name: Mapped[str] = mapped_column(String(100), nullable=False)
    rebalance_threshold: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
