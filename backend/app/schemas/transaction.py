from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from app.models.transaction import TransactionType, PaymentMethod, Mood


class TransactionCreate(BaseModel):
    type: TransactionType
    amount: Decimal
    description: str | None = None
    payment_method: PaymentMethod = PaymentMethod.CASH
    category_id: int | None = None
    account_id: int
    date: datetime | None = None
    mood: Mood | None = None
    goal_id: int | None = None


class TransactionUpdate(BaseModel):
    type: TransactionType | None = None
    amount: Decimal | None = None
    description: str | None = None
    payment_method: PaymentMethod | None = None
    category_id: int | None = None
    mood: Mood | None = None
    goal_id: int | None = None


class TransactionOut(BaseModel):
    id: int
    type: TransactionType
    amount: Decimal
    description: str | None
    payment_method: PaymentMethod
    mood: Mood | None
    date: datetime
    is_auto_categorized: bool
    ai_confidence: float | None
    category_id: int | None
    account_id: int
    user_id: int
    created_at: datetime

    model_config = {"from_attributes": True}
