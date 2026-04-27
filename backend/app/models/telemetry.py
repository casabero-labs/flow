"""TelemetryEvent model — data-driven development."""
from datetime import datetime
from sqlalchemy import String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class TelemetryEvent(Base):
    __tablename__ = "telemetry_events"

    id: Mapped[int] = mapped_column(primary_key=True)
    event_type: Mapped[str] = mapped_column(String(100))  # page_view, button_click, etc.
    event_data: Mapped[str] = mapped_column(Text)  # JSON
    user_id: Mapped[int | None] = mapped_column(default=None)
    session_id: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
