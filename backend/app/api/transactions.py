"""Transactions API routes."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract
from datetime import datetime

from app.database import get_db
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionOut, TransactionUpdate
from app.services.ai_categorizer import AICategorizer
from app.api.deps import get_current_user, get_partner_id

router = APIRouter()


@router.get("/", response_model=list[TransactionOut])
async def list_transactions(
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    month: str | None = Query(None),
    category_id: int | None = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Lista transacciones del usuario y su partner (si hay)."""
    partner_id = await get_partner_id(user.id, db)
    user_ids = [user.id] if partner_id is None else [user.id, partner_id]

    stmt = select(Transaction).where(Transaction.user_id.in_(user_ids)).order_by(Transaction.date.desc())
    if month:
        year, m = month.split("-")
        stmt = stmt.where(
            extract("year", Transaction.date) == int(year),
            extract("month", Transaction.date) == int(m),
        )
    if category_id:
        stmt = stmt.where(Transaction.category_id == category_id)
    stmt = stmt.offset(offset).limit(limit)
    result = await db.execute(stmt)
    return result.scalars().all()


@router.post("/", response_model=TransactionOut, status_code=201)
async def create_transaction(
    data: TransactionCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Registra una nueva transacción."""
    confidence = None
    auto_categorized = False

    # Auto-categorización con IA si no se provee categoría
    if data.category_id is None and data.description:
        categorizer = AICategorizer(db)
        category_id, confidence = await categorizer.categorize(data.description)
        if category_id:
            data.category_id = category_id
            auto_categorized = True

    tx = Transaction(
        user_id=user.id,
        account_id=data.account_id,
        type=data.type,
        amount=data.amount,
        description=data.description,
        payment_method=data.payment_method,
        category_id=data.category_id,
        mood=data.mood,
        goal_id=data.goal_id,
        date=data.date or datetime.utcnow(),
        ai_confidence=confidence,
        is_auto_categorized=auto_categorized,
    )
    db.add(tx)
    await db.commit()
    await db.refresh(tx)
    return tx


@router.get("/summary", response_model=dict)
async def transaction_summary(
    month: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Resumen de transacciones del mes (usuario + partner si aplica)."""
    from app.models.transaction import TransactionType
    year, m = (month or datetime.utcnow().strftime("%Y-%m")).split("-")

    partner_id = await get_partner_id(user.id, db)
    user_ids = [user.id] if partner_id is None else [user.id, partner_id]

    income_q = await db.execute(
        select(func.coalesce(func.sum(Transaction.amount), 0))
        .where(
            Transaction.user_id.in_(user_ids),
            Transaction.type == TransactionType.INCOME,
            extract("year", Transaction.date) == int(year),
            extract("month", Transaction.date) == int(m),
        )
    )
    expense_q = await db.execute(
        select(func.coalesce(func.sum(Transaction.amount), 0))
        .where(
            Transaction.user_id.in_(user_ids),
            Transaction.type == TransactionType.EXPENSE,
            extract("year", Transaction.date) == int(year),
            extract("month", Transaction.date) == int(m),
        )
    )
    income = income_q.scalar() or 0
    expense = expense_q.scalar() or 0
    return {
        "month": f"{year}-{m}",
        "income": float(income),
        "expense": float(expense),
        "balance": float(income - expense),
        "transaction_count": await db.execute(
            select(func.count(Transaction.id))
            .where(
                Transaction.user_id.in_(user_ids),
                extract("year", Transaction.date) == int(year),
                extract("month", Transaction.date) == int(m),
            )
        )
    }


@router.get("/{transaction_id}", response_model=TransactionOut)
async def get_transaction(
    transaction_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    partner_id = await get_partner_id(user.id, db)
    user_ids = [user.id] if partner_id is None else [user.id, partner_id]
    result = await db.execute(
        select(Transaction).where(
            Transaction.id == transaction_id,
            Transaction.user_id.in_(user_ids),
        )
    )
    tx = result.scalar_one_or_none()
    if not tx:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return tx


@router.patch("/{transaction_id}", response_model=TransactionOut)
async def update_transaction(
    transaction_id: int,
    data: TransactionUpdate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    partner_id = await get_partner_id(user.id, db)
    user_ids = [user.id] if partner_id is None else [user.id, partner_id]
    result = await db.execute(
        select(Transaction).where(
            Transaction.id == transaction_id,
            Transaction.user_id.in_(user_ids),
        )
    )
    tx = result.scalar_one_or_none()
    if not tx:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(tx, key, value)
    await db.commit()
    await db.refresh(tx)
    return tx


@router.delete("/{transaction_id}", status_code=204)
async def delete_transaction(
    transaction_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    result = await db.execute(
        select(Transaction).where(
            Transaction.id == transaction_id,
            Transaction.user_id == user.id,
        )
    )
    tx = result.scalar_one_or_none()
    if not tx:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    await db.delete(tx)
    await db.commit()
