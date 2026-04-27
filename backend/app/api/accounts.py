"""Accounts API routes."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models.account import Account
from app.schemas.account import AccountCreate, AccountOut

router = APIRouter()


@router.get("/", response_model=list[AccountOut])
async def list_accounts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Account))
    return result.scalars().all()


@router.post("/", response_model=AccountOut, status_code=201)
async def create_account(data: AccountCreate, db: AsyncSession = Depends(get_db)):
    account = Account(**data.model_dump())
    db.add(account)
    await db.commit()
    await db.refresh(account)
    return account


@router.delete("/{account_id}", status_code=204)
async def delete_account(account_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Account).where(Account.id == account_id))
    acc = result.scalar_one_or_none()
    if not acc:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    await db.delete(acc)
    await db.commit()
