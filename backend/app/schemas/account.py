from pydantic import BaseModel


class AccountCreate(BaseModel):
    name: str
    account_type: str = "cash"  # cash, bank, digital
    currency: str = "COP"
    is_shared: bool = False


class AccountOut(BaseModel):
    id: int
    name: str
    account_type: str
    currency: str
    user_id: int
    is_shared: bool

    model_config = {"from_attributes": True}
