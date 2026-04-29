"""Budgets API routes."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract

from app.database import get_db
from app.models.budget import Budget
from app.models.transaction import Transaction, TransactionType
from app.models.user import User
from app.schemas.budget import BudgetCreate, BudgetOut
from app.api.deps import get_current_user, get_partner_id

router = APIRouter()


@router.get("/", response_model=list[BudgetOut])
async def list_budgets(
    month: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Lista presupuestos del usuario y su partner (si hay)."""
    partner_id = await get_partner_id(user.id, db)
    user_ids = [user.id] if partner_id is None else [user.id, partner_id]

    stmt = select(Budget).where(Budget.user_id.in_(user_ids))
    if month:
        stmt = stmt.where(Budget.month == month)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("/", response_model=BudgetOut, status_code=201)
async def create_budget(
    data: BudgetCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Crea un presupuesto propio."""
    budget = Budget(**data.model_dump(), user_id=user.id)
    db.add(budget)
    await db.commit()
    await db.refresh(budget)
    return budget


@router.get("/alerts")
async def budget_alerts(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Retorna alertas de presupuestos que están cerca o sobre el límite."""
    from datetime import datetime
    month = datetime.utcnow().strftime("%Y-%m")
    year, m = month.split("-")

    partner_id = await get_partner_id(user.id, db)
    user_ids = [user.id] if partner_id is None else [user.id, partner_id]

    result = await db.execute(
        select(Budget).where(Budget.user_id.in_(user_ids), Budget.month == month)
    )
    budgets = result.scalars().all()

    alerts = []
    for b in budgets:
        spent_q = await db.execute(
            select(func.coalesce(func.sum(Transaction.amount), 0))
            .where(
                Transaction.user_id.in_(user_ids),
                Transaction.category_id == b.category_id,
                Transaction.type == TransactionType.EXPENSE,
                extract("year", Transaction.date) == int(year),
                extract("month", Transaction.date) == int(m),
            )
        )
        spent = spent_q.scalar() or 0
        pct = float(spent) / float(b.limit_amount) * 100 if b.limit_amount else 0

        if pct >= 100 and not b.alert_100_sent:
            alerts.append({"category_id": b.category_id, "percentage": pct, "alert_type": "100%", "spent": float(spent), "limit": float(b.limit_amount)})
            b.alert_100_sent = True
        elif pct >= 80 and not b.alert_80_sent:
            alerts.append({"category_id": b.category_id, "percentage": pct, "alert_type": "80%", "spent": float(spent), "limit": float(b.limit_amount)})
            b.alert_80_sent = True

    await db.commit()
    return alerts


@router.delete("/{budget_id}", status_code=204)
async def delete_budget(
    budget_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Elimina un presupuesto propio."""
    result = await db.execute(select(Budget).where(Budget.id == budget_id, Budget.user_id == user.id))
    b = result.scalar_one_or_none()
    if not b:
        raise HTTPException(status_code=404, detail="Presupuesto no encontrado")
    await db.delete(b)
    await db.commit()
