from datetime import datetime
from pydantic import BaseModel


class InsightOut(BaseModel):
    id: int
    type: str
    title: str
    description: str
    severity: str
    is_read: bool
    generated_at: datetime

    model_config = {"from_attributes": True}
