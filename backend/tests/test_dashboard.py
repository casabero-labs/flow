"""
Tests de dashboard — datos agregados, monthly_trend, category_totals.

Cubre:
- Dashboard básico con cero transacciones
- Dashboard con ingresos y gastos
- Dashboard sin autenticación
"""
import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


async def _create_account(async_client, headers) -> int:
    resp = await async_client.post(
        "/api/v1/accounts/",
        json={"name": "Test", "account_type": "cash"},
        headers=headers,
    )
    return resp.json()["id"]


async def _create_category(async_client, headers) -> int:
    # Usar categorías default
    list_resp = await async_client.get("/api/v1/categories/", headers=headers)
    cats = list_resp.json()
    if cats:
        return cats[0]["id"]
    resp = await async_client.post(
        "/api/v1/categories/",
        json={"name": "Dash Cat"},
        headers=headers,
    )
    return resp.json()["id"]


class TestDashboard:
    """GET /api/v1/dashboard/"""

    async def test_dashboard_empty(self, async_client, auth_headers):
        """Dashboard sin transacciones debe retornar ceros."""
        resp = await async_client.get("/api/v1/dashboard/", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert float(data["current_balance"]) == 0
        assert float(data["income_this_month"]) == 0
        assert float(data["expense_this_month"]) == 0
        assert float(data["balance_this_month"]) == 0
        assert isinstance(data["category_totals"], list)
        assert isinstance(data["monthly_trend"], list)
        assert len(data["monthly_trend"]) == 6  # últimos 6 meses

    async def test_dashboard_with_transactions(self, async_client, auth_headers):
        """Dashboard con datos debe reflejar ingresos y gastos."""
        account_id = await _create_account(async_client, auth_headers)
        cat_id = await _create_category(async_client, auth_headers)

        # Ingreso
        await async_client.post(
            "/api/v1/transactions/",
            json={
                "type": "income",
                "amount": "3000",
                "account_id": account_id,
            },
            headers=auth_headers,
        )

        # Gasto en categoría
        await async_client.post(
            "/api/v1/transactions/",
            json={
                "type": "expense",
                "amount": "800",
                "account_id": account_id,
                "category_id": cat_id,
            },
            headers=auth_headers,
        )

        resp = await async_client.get("/api/v1/dashboard/", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert float(data["income_this_month"]) == 3000.0
        assert float(data["expense_this_month"]) == 800.0
        assert float(data["balance_this_month"]) == 2200.0
        assert float(data["current_balance"]) == 2200.0

        # Verificar que category_totals tenga datos
        assert len(data["category_totals"]) >= 1

    async def test_dashboard_without_auth(self, async_client):
        resp = await async_client.get("/api/v1/dashboard/")
        assert resp.status_code == 401

    async def test_dashboard_monthly_trend_structure(self, async_client, auth_headers):
        """Cada entrada de monthly_trend debe tener month, income, expense, balance."""
        resp = await async_client.get("/api/v1/dashboard/", headers=auth_headers)
        data = resp.json()
        for entry in data["monthly_trend"]:
            assert "month" in entry
            assert "income" in entry
            assert "expense" in entry
            assert "balance" in entry
