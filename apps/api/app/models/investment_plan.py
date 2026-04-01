from sqlalchemy import Enum, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class InvestmentPlan(Base):
    __tablename__ = "investment_plan"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    total_budget: Mapped[float] = mapped_column(Numeric(18, 2), nullable=False)
    months: Mapped[int] = mapped_column(nullable=False)
    first_month_ratio: Mapped[float] = mapped_column(Numeric(10, 4), nullable=False)
    status: Mapped[str] = mapped_column(
        Enum("draft", "in_progress", "completed", "paused", name="plan_status_enum"),
        nullable=False,
        default="draft",
    )
