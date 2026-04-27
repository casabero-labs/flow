"""Account model."""
from datetime import datetime
from sqlalchemy import String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Account(Base):
    __tablename__ = "accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))  # Efectivo, Banco, Nequi, etc.
    account_type: Mapped[str] = mapped_column(String(50))  # cash, bank, digital
    currency: Mapped[str] = mapped_column(String(3), default="COP")
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="cascade"))
    is_shared: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="accounts")
    transactions: Mapped[list["Transaction"]] = relationship(back_populates="account", cascade="all, delete-orphan")
