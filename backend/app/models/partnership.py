"""Partnership model — Joseph y Luz."""
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Partnership(Base):
    __tablename__ = "partnerships"
    __table_args__ = (
        UniqueConstraint("inviter_id", name="uq_partnership_inviter"),
        UniqueConstraint("invitee_id", name="uq_partnership_invitee"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    inviter_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    invitee_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    invite_code: Mapped[str] = mapped_column(String(6), unique=True, index=True)
    status: Mapped[str] = mapped_column(String(20), default="pending")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    activated_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
