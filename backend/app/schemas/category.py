from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    icon: str = "💰"
    color: str = "#6B7280"


class CategoryOut(BaseModel):
    id: int
    name: str
    icon: str
    color: str
    is_default: bool
    user_id: int | None

    model_config = {"from_attributes": True}
