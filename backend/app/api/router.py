"""Router principal — agrega todos los sub-routers."""
from fastapi import APIRouter

from app.api.transactions import router as transactions_router
from app.api.categories import router as categories_router
from app.api.accounts import router as accounts_router
from app.api.budgets import router as budgets_router
from app.api.goals import router as goals_router
from app.api.insights import router as insights_router
from app.api.dashboard import router as dashboard_router
from app.api.chat import router as chat_router
from app.api.auth import router as auth_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(transactions_router, prefix="/transactions", tags=["transactions"])
api_router.include_router(categories_router, prefix="/categories", tags=["categories"])
api_router.include_router(accounts_router, prefix="/accounts", tags=["accounts"])
api_router.include_router(budgets_router, prefix="/budgets", tags=["budgets"])
api_router.include_router(goals_router, prefix="/goals", tags=["goals"])
api_router.include_router(insights_router, prefix="/insights", tags=["insights"])
api_router.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(chat_router, prefix="/chat", tags=["chat"])
