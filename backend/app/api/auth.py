"""Auth routes — login, register, me."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.user import UserCreate, UserOut, UserLogin, TokenResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def register(data: UserCreate, db: AsyncSession = Depends(get_db)):
    svc = AuthService(db)
    user = await svc.register(data.email, data.password, data.name)
    return user


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    svc = AuthService(db)
    result = await svc.login(data.email, data.password)
    if not result:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return result


@router.get("/me", response_model=UserOut)
async def me(db: AsyncSession = Depends(get_db)):
    # Placeholder — se conecta con auth real después
    raise HTTPException(status_code=501, detail="Implementar con JWT")
