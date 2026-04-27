"""AI Chat service — conversational finance assistant."""
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract
from decimal import Decimal

from app.config import settings
from app.models.transaction import Transaction, TransactionType
from app.models.category import Category
from app.schemas.chat import ChatResponse


SYSTEM_PROMPT = """Eres Flow, el asistente financiero de una pareja (Joseph y Luz).
Respondes en español, de forma amigable y clara.
Tienes acceso a sus transacciones financieras para responder preguntas.
Sé conciso, máximo 3-4 oraciones.
Nunca inventes números — usa solo los datos que tienes disponibles.
Si no tienes datos para responder, di que no tienes esa información."""


class AIChatService:
    def __init__(self, db: AsyncSession, user_id: int):
        self.db = db
        self.user_id = user_id

    async def _get_context(self) -> str:
        """Prepara contexto con datos financieros recientes del usuario."""
        from datetime import datetime
        now = datetime.utcnow()
        month_str = f"{now.year}-{now.month:02d}"

        # Gastos de este mes por categoría
        result = await self.db.execute(
            select(
                Category.name,
                func.coalesce(func.sum(Transaction.amount), 0).label("total")
            )
            .join(Transaction, Transaction.category_id == Category.id, isouter=True)
            .where(
                Transaction.user_id == self.user_id,
                Transaction.type == TransactionType.EXPENSE,
                extract("year", Transaction.date) == now.year,
                extract("month", Transaction.date) == now.month,
            )
            .group_by(Category.id)
        )
        cats = result.all()

        # Ingresos y gastos totales
        income = await self.db.execute(
            select(func.coalesce(func.sum(Transaction.amount), 0))
            .where(
                Transaction.user_id == self.user_id,
                Transaction.type == TransactionType.INCOME,
                extract("year", Transaction.date) == now.year,
                extract("month", Transaction.date) == now.month,
            )
        )
        expense = await self.db.execute(
            select(func.coalesce(func.sum(Transaction.amount), 0))
            .where(
                Transaction.user_id == self.user_id,
                Transaction.type == TransactionType.EXPENSE,
                extract("year", Transaction.date) == now.year,
                extract("month", Transaction.date) == now.month,
            )
        )

        income_val = income.scalar() or Decimal("0")
        expense_val = expense.scalar() or Decimal("0")

        cat_lines = "\n".join([f"- {c.name}: ${c.total:,.0f}" for c in cats]) or "Sin datos"

        return f"""Datos del mes ({month_str}):
- Ingresos: ${income_val:,.0f}
- Gastos: ${expense_val:,.0f}
- Balance: ${income_val - expense_val:,.0f}

Gastos por categoría:
{cat_lines}"""

    async def chat(self, message: str) -> ChatResponse:
        """Procesa mensaje del usuario y retorna respuesta."""
        context = await self._get_context()

        if not settings.minimax_api_key:
            # Fallback sin IA real
            return ChatResponse(
                response="💬 Configuremos MiniMax para el chat completo. Mientras tanto, aquí van tus datos:\n\n" + context[:500],
                sources=["dashboard"],
            )

        user_prompt = f"Contexto:\n{context}\n\nPregunta: {message}"

        try:
            async with httpx.AsyncClient(timeout=30) as client:
                r = await client.post(
                    f"{settings.minimax_base_url}/text/chatcompletion_v2",
                    headers={"Authorization": f"Bearer {settings.minimax_api_key}"},
                    json={
                        "model": "MiniMax-Text-01",
                        "messages": [
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": user_prompt},
                        ],
                        "max_tokens": 300,
                        "temperature": 0.3,
                    },
                )
                r.raise_for_status()
                data = r.json()
                response_text = data["choices"][0]["messages"][-1]["text"]
                return ChatResponse(response=response_text, sources=["transactions", "categories"])
        except Exception as exc:
            return ChatResponse(
                response=f"🤖 Tuve un problema conectando con la IA: {str(exc)[:100]}",
                sources=[],
            )
