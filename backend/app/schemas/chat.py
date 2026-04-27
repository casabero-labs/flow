from pydantic import BaseModel


class ChatMessage(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    sources: list[str] = []  # categorías o datos que usó para responder
