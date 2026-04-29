"""Insights API routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.insight import Insight
from app.models.user import User
from app.schemas.insight import InsightOut
from app.api.deps import get_current_user

router = APIRouter()


@router.get("/", response_model=list[InsightOut])
async def list_insights(
    unread_only: bool = False,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Lista todos los insights (sistema)."""
    stmt = select(Insight).order_by(Insight.generated_at.desc())
    if unread_only:
        stmt = stmt.where(Insight.is_read == False)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.patch("/{insight_id}/read")
async def mark_insight_read(
    insight_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Marca un insight como leído."""
    result = await db.execute(select(Insight).where(Insight.id == insight_id))
    insight = result.scalar_one_or_none()
    if insight:
        insight.is_read = True
        await db.commit()
    return {"ok": True}
