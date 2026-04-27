"""Budgets API routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.budget import Budget
from app.schemas.budget import BudgetCreate, BudgetOut

router = APIRouter()


@router.get("/", response_model=list[BudgetOut])
async def list_budgets(month: str | None = None, db: AsyncSession = Depends(get_db)):
    stmt = select(Budget)
    if month:
        stmt = stmt.where(Budget.month == month)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("/", response_model=BudgetOut, status_code=201)
async def create_budget(data: BudgetCreate, db: AsyncSession = Depends(get_db)):
    budget = Budget(**data.model_dump())
    db.add(budget)
    await db.commit()
    await db.refresh(budget)
    return budget


@router.patch("/{budget_id}", response_model=BudgetOut)
async def update_budget(budget_id: int, data: BudgetCreate, db: AsyncSession = Depends(get_db)):
    from fastapi import HTTPException
    result = await db.execute(select(Budget).where(Budget.id == budget_id))
    b = result.scalar_one_or_none()
    if not b:
        raise HTTPException(status_code=404, detail="Presupuesto no encontrado")
    for key, value in data.model_dump().items():
        setattr(b, key, value)
    await db.commit()
    await db.refresh(b)
    return b


@router.delete("/{budget_id}", status_code=204)
async def delete_budget(budget_id: int, db: AsyncSession = Depends(get_db)):
    from fastapi import HTTPException
    result = await db.execute(select(Budget).where(Budget.id == budget_id))
    b = result.scalar_one_or_none()
    if not b:
        raise HTTPException(status_code=404, detail="Presupuesto no encontrado")
    await db.delete(b)
    await db.commit()
