"""AI Categorizer — auto-categoriza transacciones basándose en descripción."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.category import Category


CATEGORY_KEYWORDS = {
    "Comida": ["comida", "almuerzo", "cena", "desayuno", "restaurante", "cafe", "街", "pizza", "hamburguesa"],
    "Servicios": ["luz", "agua", "gas", "internet", "telefono", "servicio", "acueducto"],
    "Transporte": ["gasolina", "taxi", "uber", "bus", "metro", "transporte", "peaje", "parqueadero"],
    "Salud": ["farmacia", "medicina", "doctor", "hospital", "clinica", "salud", "medico"],
    "Ocio": ["cine", "netflix", "spotify", "juego", "entretenimiento", "concierto", "bar"],
    "Hogar": ["mueble", "casa", "electrodomestico", "ferreteria", "decoracion", "aseo"],
    "Vestuario": ["ropa", "zapato", "tienda", "vestido", "camisa", "pantalon"],
    "Ahorro": ["ahorro", "inversion", "cesantia", "fondo"],
}


class AICategorizer:
    """Categorizador simple basado en keywords. Se mejora con correcciones del usuario."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def categorize(self, description: str) -> tuple[int | None, float]:
        """Retorna (category_id, confidence) basado en keywords."""
        desc_lower = description.lower()

        best_match = None
        best_hits = 0

        for cat_name, keywords in CATEGORY_KEYWORDS.items():
            hits = sum(1 for kw in keywords if kw in desc_lower)
            if hits > best_hits:
                best_hits = hits
                best_match = cat_name

        if best_match and best_hits > 0:
            result = await self.db.execute(
                select(Category).where(Category.name == best_match)
            )
            cat = result.scalar_one_or_none()
            if cat:
                confidence = min(0.5 + best_hits * 0.15, 0.95)
                return cat.id, confidence

        # Default a "Otros"
        result = await self.db.execute(
            select(Category).where(Category.name == "Otros")
        )
        cat = result.scalar_one_or_none()
        if cat:
            return cat.id, 0.3

        return None, 0.0

    async def learn(self, transaction_description: str, category_id: int):
        """Aprende de correcciones del usuario para mejorar futuras categorizaciones."""
        # Placeholder: guardar en tabla de aprendizaje
        # Por ahora no hace nada — se puede expandir con embeddings
        pass
