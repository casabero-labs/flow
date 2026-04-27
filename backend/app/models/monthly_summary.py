"""MonthlySummary model — IA-generated narrative summaries."""
from datetime import datetime
from sqlalchemy import String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class MonthlySummary(Base):
    __tablename__ = "monthly_summaries"

    id: Mapped[int] = mapped_column(primary_key=True)
    month: Mapped[str] = mapped_column(String(7))  # "2025-02"
    narrative: Mapped[str] = mapped_column(Text)
    summary_data: Mapped[str] = mapped_column(Text)  # JSON con totales, comparativas
    generated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
