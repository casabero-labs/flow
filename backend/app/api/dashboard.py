"""Dashboard API routes."""
from decimal import Decimal
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, extract, func

from app.database import get_db
from app.models.transaction import Transaction, TransactionType
from app.models.category import Category
from app.models.user import User
from app.schemas.dashboard import DashboardOut, CategoryTotal, MonthlyBalance
from app.api.deps import get_current_user, get_partner_id

router = APIRouter()


def _current_month() -> tuple[int, int]:
    from datetime import datetime
    now = datetime.utcnow()
    return now.year, now.month


@router.get("/", response_model=DashboardOut)
async def get_dashboard(
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """Dashboard con datos del usuario y su partner (si hay partnership activo)."""
    year, month = _current_month()

    partner_id = await get_partner_id(user.id, db)
    user_ids = [user.id] if partner_id is None else [user.id, partner_id]

    # Ingresos y gastos del mes actual
    income_q = await db.execute(
        select(func.coalesce(func.sum(Transaction.amount), 0))
        .where(
            Transaction.user_id.in_(user_ids),
            Transaction.type == TransactionType.INCOME,
            extract("year", Transaction.date) == year,
            extract("month", Transaction.date) == month,
        )
    )
    income = income_q.scalar() or Decimal("0")

    expense_q = await db.execute(
        select(func.coalesce(func.sum(Transaction.amount), 0))
        .where(
            Transaction.user_id.in_(user_ids),
            Transaction.type == TransactionType.EXPENSE,
            extract("year", Transaction.date) == year,
            extract("month", Transaction.date) == month,
        )
    )
    expense = expense_q.scalar() or Decimal("0")

    # Totales por categoría (gastos del mes)
    cat_result = await db.execute(
        select(
            Category.name,
            Category.icon,
            Category.color,
            func.coalesce(func.sum(Transaction.amount), 0).label("total"),
        )
        .join(Transaction, Transaction.category_id == Category.id, isouter=True)
        .where(
            Transaction.user_id.in_(user_ids),
            Transaction.type == TransactionType.EXPENSE,
            extract("year", Transaction.date) == year,
            extract("month", Transaction.date) == month,
        )
        .group_by(Category.id)
        .order_by(func.sum(Transaction.amount).desc())
    )
    cat_rows = cat_result.all()
    total_expense = expense or Decimal("1")
    category_totals = [
        CategoryTotal(
            category=row.name,
            icon=row.icon,
            color=row.color,
            total=row.total,
            percentage=float(row.total / total_expense * 100),
        )
        for row in cat_rows
    ]

    # Tendencia mensual últimos 6 meses
    monthly_trend = []
    from datetime import datetime
    for i in range(5, -1, -1):
        m_month = month - i
        m_year = year
        while m_month <= 0:
            m_month += 12
            m_year -= 1
        m_str = f"{m_year}-{m_month:02d}"

        inc = await db.execute(
            select(func.coalesce(func.sum(Transaction.amount), 0))
            .where(
                Transaction.user_id.in_(user_ids),
                Transaction.type == TransactionType.INCOME,
                extract("year", Transaction.date) == m_year,
                extract("month", Transaction.date) == m_month,
            )
        )
        exp = await db.execute(
            select(func.coalesce(func.sum(Transaction.amount), 0))
            .where(
                Transaction.user_id.in_(user_ids),
                Transaction.type == TransactionType.EXPENSE,
                extract("year", Transaction.date) == m_year,
                extract("month", Transaction.date) == m_month,
            )
        )
        inc_val = inc.scalar() or Decimal("0")
        exp_val = exp.scalar() or Decimal("0")
        monthly_trend.append(MonthlyBalance(
            month=m_str,
            income=inc_val,
            expense=exp_val,
            balance=inc_val - exp_val,
        ))

    return DashboardOut(
        current_balance=income - expense,
        income_this_month=income,
        expense_this_month=expense,
        balance_this_month=income - expense,
        category_totals=category_totals,
        monthly_trend=monthly_trend,
        top_expense_categories=category_totals[:5],
    )
