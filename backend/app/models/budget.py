"""Budget model."""
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, DateTime, ForeignKey, Boolean
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Budget(Base):
    __tablename__ = "budgets"

    id: Mapped[int] = mapped_column(primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="cascade"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="cascade"))
    month: Mapped[str] = mapped_column(String(7))  # "2025-02"
    limit_amount: Mapped[Decimal] = mapped_column()
    alert_80_sent: Mapped[bool] = mapped_column(Boolean, default=False)
    alert_100_sent: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint("limit_amount > 0", name="positive_limit"),
    )

    category: Mapped["Category"] = relationship(back_populates="budgets")
    user: Mapped["User"] = relationship(back_populates="budgets")
