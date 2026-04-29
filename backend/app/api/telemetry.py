"""Telemetry API endpoint — data-driven development."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.telemetry import TelemetryEvent
from app.schemas.telemetry import TelemetryEventCreate
from app.api.deps import get_optional_user
from app.models.user import User

router = APIRouter()


@router.post("/", status_code=201)
async def create_telemetry_event(
    data: TelemetryEventCreate,
    db: AsyncSession = Depends(get_db),
    user: User | None = Depends(get_optional_user),
):
    """Registra un evento de telemetría anónimo o autenticado."""
    import json

    event = TelemetryEvent(
        event_type=data.event_type,
        event_data=json.dumps(data.event_data),
        user_id=user.id if user else None,
        session_id=data.session_id,
    )
    db.add(event)
    await db.commit()
    return {"id": event.id, "status": "ok"}
