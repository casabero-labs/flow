"""Goals API routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.database import get_db
from app.models.goal import Goal
from app.models.goal_contribution import GoalContribution
from app.models.user import User
from app.schemas.goal import GoalCreate, GoalOut, GoalContributionCreate
from app.api.deps import get_current_user, get_partner_id

router = APIRouter()


@router.get("/", response_model=list[GoalOut])
async def list_goals(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Lista metas del usuario y su partner (si hay partnership activo)."""
    partner_id = await get_partner_id(user.id, db)
    user_ids = [user.id] if partner_id is None else [user.id, partner_id]

    result = await db.execute(select(Goal).where(Goal.user_id.in_(user_ids)).order_by(Goal.created_at.desc()))
    goals = result.scalars().all()

    enriched = []
    for goal in goals:
        contribs = await db.execute(
            select(func.coalesce(func.sum(GoalContribution.amount), 0))
            .where(GoalContribution.goal_id == goal.id)
        )
        current = contribs.scalar() or 0
        progress = float(current / float(goal.target_amount) * 100) if goal.target_amount else 0
        goal.current_amount = current
        goal.progress_pct = min(progress, 100)
        enriched.append(goal)
    return enriched


@router.post("/", response_model=GoalOut, status_code=201)
async def create_goal(
    data: GoalCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Crea una meta propia."""
    goal = Goal(**data.model_dump(), user_id=user.id)
    db.add(goal)
    await db.commit()
    await db.refresh(goal)
    return goal


@router.post("/{goal_id}/contribute", response_model=GoalOut)
async def contribute_to_goal(
    goal_id: int,
    data: GoalContributionCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Agrega una contribución a una meta (propia o del partner)."""
    partner_id = await get_partner_id(user.id, db)
    user_ids = [user.id] if partner_id is None else [user.id, partner_id]

    result = await db.execute(select(Goal).where(Goal.id == goal_id, Goal.user_id.in_(user_ids)))
    goal = result.scalar_one_or_none()
    if not goal:
        raise HTTPException(status_code=404, detail="Meta no encontrada")

    contrib = GoalContribution(goal_id=goal_id, **data.model_dump())
    db.add(contrib)
    await db.commit()

    # Recalcular progreso
    contribs = await db.execute(
        select(func.coalesce(func.sum(GoalContribution.amount), 0))
        .where(GoalContribution.goal_id == goal.id)
    )
    current = contribs.scalar() or 0
    goal.current_amount = current
    goal.progress_pct = min(float(current / float(goal.target_amount) * 100), 100)
    await db.commit()
    return goal


@router.delete("/{goal_id}", status_code=204)
async def delete_goal(
    goal_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Elimina una meta propia."""
    result = await db.execute(select(Goal).where(Goal.id == goal_id, Goal.user_id == user.id))
    goal = result.scalar_one_or_none()
    if not goal:
        raise HTTPException(status_code=404, detail="Meta no encontrada")
    await db.delete(goal)
    await db.commit()
