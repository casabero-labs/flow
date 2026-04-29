"""Schemas de Partnership."""
from datetime import datetime
from pydantic import BaseModel


class PartnershipInviteOut(BaseModel):
    id: int
    invite_code: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class PartnershipJoinIn(BaseModel):
    invite_code: str


class UserOut(BaseModel):
    id: int
    email: str
    name: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}


class PartnershipStatusOut(BaseModel):
    id: int
    inviter: UserOut
    invitee: UserOut | None
    status: str
    created_at: datetime
    activated_at: datetime | None

    model_config = {"from_attributes": True}
