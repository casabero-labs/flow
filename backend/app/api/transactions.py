"""Transactions API routes."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime

from app.database import get_db
from app.models.transaction import Transaction
from app.models.category import Category
from app.schemas.transaction import TransactionCreate, TransactionOut, TransactionUpdate
from app.services.ai_categorizer import AICategorizer

router = APIRouter()


@router.get("/", response_model=list[TransactionOut])
async def list_transactions(
    limit: int = 50,
    offset: int = 0,
    month: str | None = None,
    category_id: int | None = None,
    db: AsyncSession = Depends(get_db),
):
    """Lista transacciones con filtros."""
    stmt = select(Transaction).order_by(Transaction.date.desc())
    if month:
        year, m = month.split("-")
        from sqlalchemy import extract
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
):
    """Registra una nueva transacción."""
    # Auto-categorización con IA si no seprovee categoría
    if data.category_id is None and data.description:
        categorizer = AICategorizer(db)
        category_id, confidence = await categorizer.categorize(data.description)
        data.category_id = category_id
        # Guardar confidence si se categorizó automáticamente
    else:
        confidence = None

    transaction = Transaction(
        **data.model_dump(),
        ai_confidence=confidence,
    )
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)
    return transaction


@router.get("/{transaction_id}", response_model=TransactionOut)
async def get_transaction(transaction_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Transaction).where(Transaction.id == transaction_id))
    tx = result.scalar_one_or_none()
    if not tx:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return tx


@router.patch("/{transaction_id}", response_model=TransactionOut)
async def update_transaction(
    transaction_id: int,
    data: TransactionUpdate,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Transaction).where(Transaction.id == transaction_id))
    tx = result.scalar_one_or_none()
    if not tx:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(tx, key, value)
    await db.commit()
    await db.refresh(tx)
    return tx


@router.delete("/{transaction_id}", status_code=204)
async def delete_transaction(transaction_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Transaction).where(Transaction.id == transaction_id))
    tx = result.scalar_one_or_none()
    if not tx:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    await db.delete(tx)
    await db.commit()
