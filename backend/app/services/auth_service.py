"""Auth service."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

from app.config import settings
from app.models.user import User
from app.schemas.user import TokenResponse, UserOut

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register(self, email: str, password: str, name: str) -> User:
        hashed = pwd_context.hash(password)
        user = User(email=email, hashed_password=hashed, name=name)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def login(self, email: str, password: str) -> TokenResponse | None:
        result = await self.db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user or not pwd_context.verify(password, user.hashed_password):
            return None
        token = jwt.encode(
            {"sub": str(user.id), "exp": datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)},
            settings.secret_key,
            algorithm=settings.algorithm,
        )
        return TokenResponse(
            access_token=token,
            user=UserOut.model_validate(user),
        )
