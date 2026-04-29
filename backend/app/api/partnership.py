"""Partnership API routes."""
import secrets
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_

from app.database import get_db
from app.models.partnership import Partnership
from app.models.user import User
from app.schemas.partnership import PartnershipInviteOut, PartnershipJoinIn, PartnershipStatusOut, UserOut
from app.api.deps import get_current_user, get_partner_id

router = APIRouter()

INVITE_CODE_LENGTH = 6


def _generate_code() -> str:
    """Genera un código alfanumérico de 6 caracteres."""
    return secrets.token_urlsafe(INVITE_CODE_LENGTH)[:INVITE_CODE_LENGTH].upper()


@router.post("/invite", response_model=PartnershipInviteOut)
async def create_invite(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Genera un código de invitación para asociarse con otra persona."""
    # No puede invitar si ya tiene partnership activo
    partner_id = await get_partner_id(user.id, db)
    if partner_id is not None:
        raise HTTPException(status_code=400, detail="Ya tienes un partnership activo")

    # No puede invitar si ya tiene una invitación pendiente
    existing = await db.execute(
        select(Partnership).where(
            Partnership.inviter_id == user.id,
            Partnership.status == "pending",
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Ya tienes una invitación pendiente")

    # Generar código único
    code = _generate_code()
    while True:
        dup = await db.execute(select(Partnership).where(Partnership.invite_code == code))
        if not dup.scalar_one_or_none():
            break
        code = _generate_code()

    partnership = Partnership(
        inviter_id=user.id,
        invite_code=code,
        status="pending",
    )
    db.add(partnership)
    await db.commit()
    await db.refresh(partnership)
    return partnership


@router.post("/join", response_model=PartnershipStatusOut)
async def join_partnership(
    data: PartnershipJoinIn,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Se une a un partnership usando un código de invitación."""
    code = data.invite_code.strip().upper()

    # Buscar partnership con código
    result = await db.execute(select(Partnership).where(Partnership.invite_code == code))
    partnership = result.scalar_one_or_none()

    if not partnership:
        raise HTTPException(status_code=404, detail="Código de invitación no válido")

    if partnership.status != "pending":
        raise HTTPException(status_code=400, detail="Esta invitación ya no está disponible")

    if partnership.inviter_id == user.id:
        raise HTTPException(status_code=400, detail="No puedes unirte a tu propia invitación")

    # Verificar que el invitado no tenga ya partnership activo
    partner_id = await get_partner_id(user.id, db)
    if partner_id is not None:
        raise HTTPException(status_code=400, detail="Ya tienes un partnership activo")

    from datetime import datetime
    partnership.invitee_id = user.id
    partnership.status = "active"
    partnership.activated_at = datetime.utcnow()
    await db.commit()
    await db.refresh(partnership)

    # Cargar usuarios para la respuesta
    inviter_result = await db.execute(select(User).where(User.id == partnership.inviter_id))
    inviter = inviter_result.scalar_one()
    invitee_result = await db.execute(select(User).where(User.id == partnership.invitee_id))
    invitee = invitee_result.scalar_one()

    return PartnershipStatusOut(
        id=partnership.id,
        inviter=UserOut.model_validate(inviter),
        invitee=UserOut.model_validate(invitee),
        status=partnership.status,
        created_at=partnership.created_at,
        activated_at=partnership.activated_at,
    )


@router.get("/status", response_model=PartnershipStatusOut)
async def get_partnership_status(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Retorna el estado actual del partnership del usuario."""
    partner_id = await get_partner_id(user.id, db)

    if partner_id is None:
        raise HTTPException(status_code=404, detail="No tienes un partnership activo")

    result = await db.execute(
        select(Partnership).where(
            or_(
                and_(Partnership.inviter_id == user.id, Partnership.status == "active"),
                and_(Partnership.invitee_id == user.id, Partnership.status == "active"),
            )
        )
    )
    partnership = result.scalar_one_or_none()

    if not partnership:
        raise HTTPException(status_code=404, detail="No tienes un partnership activo")

    inviter_result = await db.execute(select(User).where(User.id == partnership.inviter_id))
    inviter = inviter_result.scalar_one()
    invitee_result = await db.execute(select(User).where(User.id == partnership.invitee_id))
    invitee = invitee_result.scalar_one()

    return PartnershipStatusOut(
        id=partnership.id,
        inviter=UserOut.model_validate(inviter),
        invitee=UserOut.model_validate(invitee),
        status=partnership.status,
        created_at=partnership.created_at,
        activated_at=partnership.activated_at,
    )


@router.delete("/", status_code=204)
async def delete_partnership(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Rompe el partnership activo."""
    result = await db.execute(
        select(Partnership).where(
            or_(
                and_(Partnership.inviter_id == user.id, Partnership.status == "active"),
                and_(Partnership.invitee_id == user.id, Partnership.status == "active"),
            )
        )
    )
    partnership = result.scalar_one_or_none()
    if not partnership:
        raise HTTPException(status_code=404, detail="No tienes un partnership activo")

    await db.delete(partnership)
    await db.commit()
