"""Goals API routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from decimal import Decimal

from app.database import get_db
from app.models.goal import Goal, GoalContribution
from app.models.transaction import Transaction
from app.schemas.goal import GoalCreate, GoalOut, GoalContributionCreate

router = APIRouter()


@router.get("/", response_model=list[GoalOut])
async def list_goals(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Goal).order_by(Goal.created_at.desc()))
    goals = result.scalars().all()

    # Calcular progreso para cada meta
    enriched = []
    for goal in goals:
        contribs = await db.execute(
            select(func.coalesce(func.sum(GoalContribution.amount), 0))
            .where(GoalContribution.goal_id == goal.id)
        )
        current = contribs.scalar() or Decimal("0")
        progress = float(current / goal.target_amount * 100) if goal.target_amount else 0
        goal.current_amount = current
        goal.progress_pct = min(progress, 100)
        enriched.append(goal)
    return enriched


@router.post("/", response_model=GoalOut, status_code=201)
async def create_goal(data: GoalCreate, db: AsyncSession = Depends(get_db)):
    goal = Goal(**data.model_dump())
    db.add(goal)
    await db.commit()
    await db.refresh(goal)
    return goal


@router.post("/{goal_id}/contribute", response_model=GoalOut)
async def contribute_to_goal(
    goal_id: int,
    data: GoalContributionCreate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Goal).where(Goal.id == goal_id))
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
    current = contribs.scalar() or Decimal("0")
    goal.current_amount = current
    goal.progress_pct = min(float(current / goal.target_amount * 100), 100)
    await db.commit()
    return goal


@router.delete("/{goal_id}", status_code=204)
async def delete_goal(goal_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Goal).where(Goal.id == goal_id))
    goal = result.scalar_one_or_none()
    if not goal:
        raise HTTPException(status_code=404, detail="Meta no encontrada")
    await db.delete(goal)
    await db.commit()
