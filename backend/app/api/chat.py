"""Chat IA — conversaciones sobre finanzas."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.schemas.chat import ChatMessage, ChatResponse
from app.services.ai_chat import AIChatService
from app.api.deps import get_current_user

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat(
    message: ChatMessage,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    svc = AIChatService(db, user.id)
    response = await svc.chat(message.message)
    return response
