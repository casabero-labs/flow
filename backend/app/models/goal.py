"""Goal model."""
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Goal(Base):
    __tablename__ = "goals"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    emoji: Mapped[str] = mapped_column(String(10), default="🎯")
    target_amount: Mapped[Decimal] = mapped_column()
    deadline: Mapped[datetime | None] = mapped_column(nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="cascade"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="goals")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="goal")
    contributions: Mapped[list["GoalContribution"]] = relationship(
        back_populates="goal", cascade="all, delete-orphan"
    )

# Import at bottom to avoid circular
from app.models.goal_contribution import GoalContribution
