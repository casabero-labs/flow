"""Pydantic schema for telemetry events."""
from pydantic import BaseModel


class TelemetryEventCreate(BaseModel):
    event_type: str  # page_view, button_click, feature_use, etc.
    event_data: dict = {}
    session_id: str | None = None
