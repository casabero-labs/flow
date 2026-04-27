from datetime import datetime
from pydantic import BaseModel


class MonthlySummaryOut(BaseModel):
    id: int
    month: str
    narrative: str
    summary_data: str  # JSON
    generated_at: datetime

    model_config = {"from_attributes": True}
