from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel


class GoalContributionCreate(BaseModel):
    amount: Decimal
    note: str | None = None


class GoalOut(BaseModel):
    id: int
    name: str
    emoji: str
    target_amount: Decimal
    deadline: datetime | None
    user_id: int
    current_amount: Decimal | None = None
    progress_pct: float | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
