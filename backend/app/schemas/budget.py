from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class BudgetCreate(BaseModel):
    category_id: int
    month: str  # "2025-02"
    limit_amount: Decimal


class BudgetOut(BaseModel):
    id: int
    category_id: int
    user_id: int
    month: str
    limit_amount: Decimal
    alert_80_sent: bool
    alert_100_sent: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class BudgetAlert(BaseModel):
    category_name: str
    month: str
    spent: Decimal
    limit: Decimal
    percentage: float
    alert_type: str  # "80%" or "100%"
