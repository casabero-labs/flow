"""Chat IA — conversaciones sobre finanzas."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.chat import ChatMessage, ChatResponse
from app.services.ai_chat import AIChatService

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat(
    message: ChatMessage,
    db: AsyncSession = Depends(get_db),
):
    svc = AIChatService(db)
    response = await svc.chat(message.message)
    return response
