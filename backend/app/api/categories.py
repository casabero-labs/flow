"""Categories API routes."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_

from app.database import get_db
from app.models.category import Category
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryOut
from app.api.deps import get_current_user, get_partner_id

router = APIRouter()

DEFAULT_CATEGORIES = [
    {"name": "Comida", "icon": "🍔", "color": "#F87171", "is_default": True},
    {"name": "Servicios", "icon": "💡", "color": "#FBBF24", "is_default": True},
    {"name": "Transporte", "icon": "🚗", "color": "#60A5FA", "is_default": True},
    {"name": "Salud", "icon": "🏥", "color": "#34D399", "is_default": True},
    {"name": "Ocio", "icon": "🎬", "color": "#A78BFA", "is_default": True},
    {"name": "Hogar", "icon": "🏠", "color": "#FB923C", "is_default": True},
    {"name": "Vestuario", "icon": "👕", "color": "#F472B6", "is_default": True},
    {"name": "Ahorro", "icon": "💰", "color": "#10B981", "is_default": True},
    {"name": "Otros", "icon": "📦", "color": "#6B7280", "is_default": True},
]


@router.get("/", response_model=list[CategoryOut])
async def list_categories(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Lista categorías del usuario y su partner (si hay)."""
    partner_id = await get_partner_id(user.id, db)
    if partner_id is None:
        result = await db.execute(select(Category).order_by(Category.is_default.desc(), Category.name))
    else:
        result = await db.execute(
            select(Category).where(
                or_(Category.user_id == None, Category.user_id == user.id, Category.user_id == partner_id)
            ).order_by(Category.is_default.desc(), Category.name)
        )
    cats = result.scalars().all()
    if not cats:
        for cat_data in DEFAULT_CATEGORIES:
            db.add(Category(**cat_data, user_id=user.id))
        await db.commit()
        result = await db.execute(select(Category).order_by(Category.is_default.desc(), Category.name))
        cats = result.scalars().all()
    return cats


@router.post("/", response_model=CategoryOut, status_code=201)
async def create_category(
    data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Crea una categoría propia."""
    cat = Category(**data.model_dump(), is_default=False, user_id=user.id)
    db.add(cat)
    await db.commit()
    await db.refresh(cat)
    return cat


@router.delete("/{category_id}", status_code=204)
async def delete_category(
    category_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    from fastapi import HTTPException
    result = await db.execute(select(Category).where(Category.id == category_id))
    cat = result.scalar_one_or_none()
    if not cat:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    if cat.is_default:
        raise HTTPException(status_code=400, detail="No se pueden borrar categorías default")
    if cat.user_id and cat.user_id != user.id:
        raise HTTPException(status_code=403, detail="No tienes permiso")
    await db.delete(cat)
    await db.commit()
