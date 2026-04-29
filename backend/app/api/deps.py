"""Dependencias de autenticación."""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_

from app.database import get_db
from app.models.user import User
from app.models.partnership import Partnership
from app.config import settings
from jose import jwt, JWTError

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Extrae el usuario actual del token JWT."""
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail="Usuario no encontrado")
    return user


async def get_optional_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(HTTPBearer(auto_error=False)),
    db: AsyncSession = Depends(get_db),
) -> User | None:
    """Usuario opcional — retorna None si no hay token."""
    if credentials is None:
        return None
    try:
        return await get_current_user(credentials, db)
    except HTTPException:
        return None


async def get_partner_id(user_id: int, db: AsyncSession) -> int | None:
    """Retorna el ID del partner activo o None si no hay partnership."""
    result = await db.execute(
        select(Partnership).where(
            or_(
                and_(Partnership.inviter_id == user_id, Partnership.status == "active"),
                and_(Partnership.invitee_id == user_id, Partnership.status == "active"),
            )
        )
    )
    partnership = result.scalar_one_or_none()
    if partnership is None:
        return None
    return partnership.invitee_id if partnership.inviter_id == user_id else partnership.inviter_id
