"""Transaction model."""
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.database import Base


class TransactionType(str, enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"


class PaymentMethod(str, enum.Enum):
    CASH = "cash"
    CARD = "card"
    TRANSFER = "transfer"
    OTHER = "other"


class Mood(str, enum.Enum):
    HAPPY = "happy"  # 😊
    NEUTRAL = "neutral"  # 😐
    STRESSED = "stressed"  # 😰
    FRUSTRATED = "frustrated"  # 😤
    ANXIOUS = "anxious"  # 😟


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[TransactionType] = mapped_column(SQLEnum(TransactionType))
    amount: Mapped[Decimal] = mapped_column()  # siempre positivo
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    payment_method: Mapped[PaymentMethod] = mapped_column(SQLEnum(PaymentMethod), default=PaymentMethod.CASH)

    # Relaciones
    category_id: Mapped[int | None] = mapped_column(ForeignKey("categories.id", ondelete="set null"), nullable=True)
    account_id: Mapped[int] = mapped_column(ForeignKey("accounts.id", ondelete="cascade"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="cascade"))
    goal_id: Mapped[int | None] = mapped_column(ForeignKey("goals.id", ondelete="set null"), nullable=True)

    # Mood tracking
    mood: Mapped[Mood | None] = mapped_column(SQLEnum(Mood), nullable=True)

    # IA
    is_auto_categorized: Mapped[bool] = mapped_column(Boolean, default=False)
    ai_confidence: Mapped[float | None] = mapped_column(default=None)  # 0.0 - 1.0

    # Fechas
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    # Relations
    category: Mapped["Category | None"] = relationship(back_populates="transactions")
    account: Mapped["Account"] = relationship(back_populates="transactions")
    user: Mapped["User"] = relationship(back_populates="transactions")
    goal: Mapped["Goal | None"] = relationship(back_populates="transactions")
