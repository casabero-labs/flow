from decimal import Decimal
from pydantic import BaseModel


class CategoryTotal(BaseModel):
    category: str
    icon: str
    color: str
    total: Decimal
    percentage: float


class MonthlyBalance(BaseModel):
    month: str
    income: Decimal
    expense: Decimal
    balance: Decimal


class DashboardOut(BaseModel):
    current_balance: Decimal
    income_this_month: Decimal
    expense_this_month: Decimal
    balance_this_month: Decimal
    category_totals: list[CategoryTotal]
    monthly_trend: list[MonthlyBalance]
    top_expense_categories: list[CategoryTotal]
