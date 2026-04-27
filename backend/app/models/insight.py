"""Insight model — IA-generated insights."""
from datetime import datetime
from sqlalchemy import String, DateTime, Text, Boolean
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.database import Base


class InsightType(str, enum.Enum):
    MOOD_CORRELATION = "mood_correlation"
    ANOMALY = "anomaly"
    GOAL_ALERT = "goal_alert"
    BUDGET_ALERT = "budget_alert"
    SPENDING_TREND = "spending_trend"


class Insight(Base):
    __tablename__ = "insights"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[InsightType] = mapped_column(SQLEnum(InsightType))
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text)
    severity: Mapped[str] = mapped_column(String(20), default="info")  # low, medium, high
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
