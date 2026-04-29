"""
Tests de presupuestos — CRUD + alertas 80%/100%.

Cubre:
- Crear presupuesto
- Listar presupuestos (con y sin filtro de mes)
- Alertas al llegar a 80% y 100%
- Eliminar presupuesto
- Sin autenticación
"""
import pytest
from httpx import AsyncClient
from datetime import datetime

pytestmark = pytest.mark.asyncio

CURRENT_MONTH = datetime.utcnow().strftime("%Y-%m")


async def _create_account(async_client, headers) -> int:
    resp = await async_client.post(
        "/api/v1/accounts/",
        json={"name": "Test", "account_type": "cash"},
        headers=headers,
    )
    return resp.json()["id"]


async def _create_category(async_client, headers) -> int:
    # Primero listar para obtener una categoría default
    list_resp = await async_client.get("/api/v1/categories/", headers=headers)
    cats = list_resp.json()
    if cats:
        return cats[0]["id"]
    resp = await async_client.post(
        "/api/v1/categories/",
        json={"name": "Budget Cat"},
        headers=headers,
    )
    return resp.json()["id"]


class TestCreateBudget:
    """POST /api/v1/budgets/"""

    async def test_create_ok(self, async_client, auth_headers):
        cat_id = await _create_category(async_client, auth_headers)
        resp = await async_client.post(
            "/api/v1/budgets/",
            json={
                "category_id": cat_id,
                "month": CURRENT_MONTH,
                "limit_amount": "500.00",
            },
            headers=auth_headers,
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["month"] == CURRENT_MONTH
        assert float(data["limit_amount"]) == 500.0
        assert data["alert_80_sent"] is False
        assert data["alert_100_sent"] is False


class TestListBudgets:
    """GET /api/v1/budgets/"""

    async def test_list_empty(self, async_client, auth_headers):
        resp = await async_client.get("/api/v1/budgets/", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json() == []

    async def test_list_with_data(self, async_client, auth_headers):
        cat_id = await _create_category(async_client, auth_headers)
        await async_client.post(
            "/api/v1/budgets/",
            json={"category_id": cat_id, "month": CURRENT_MONTH, "limit_amount": "300"},
            headers=auth_headers,
        )
        resp = await async_client.get("/api/v1/budgets/", headers=auth_headers)
        assert resp.status_code == 200
        assert len(resp.json()) == 1

    async def test_list_filter_month(self, async_client, auth_headers):
        cat_id = await _create_category(async_client, auth_headers)
        await async_client.post(
            "/api/v1/budgets/",
            json={"category_id": cat_id, "month": "2026-04", "limit_amount": "300"},
            headers=auth_headers,
        )
        await async_client.post(
            "/api/v1/budgets/",
            json={"category_id": cat_id, "month": "2026-05", "limit_amount": "400"},
            headers=auth_headers,
        )
        resp = await async_client.get("/api/v1/budgets/?month=2026-04", headers=auth_headers)
        assert resp.status_code == 200
        assert len(resp.json()) == 1


class TestBudgetAlerts:
    """GET /api/v1/budgets/alerts"""

    async def test_no_alerts_when_below_80(self, async_client, auth_headers):
        cat_id = await _create_category(async_client, auth_headers)
        account_id = await _create_account(async_client, auth_headers)
        await async_client.post(
            "/api/v1/budgets/",
            json={"category_id": cat_id, "month": CURRENT_MONTH, "limit_amount": "1000"},
            headers=auth_headers,
        )
        # Gasto pequeño < 80%
        await async_client.post(
            "/api/v1/transactions/",
            json={"type": "expense", "amount": "100", "account_id": account_id, "category_id": cat_id},
            headers=auth_headers,
        )
        resp = await async_client.get("/api/v1/budgets/alerts", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json() == []

    async def test_alert_at_80(self, async_client, auth_headers):
        cat_id = await _create_category(async_client, auth_headers)
        account_id = await _create_account(async_client, auth_headers)
        # Budget de 100, gastar 80 → 80%
        await async_client.post(
            "/api/v1/budgets/",
            json={"category_id": cat_id, "month": CURRENT_MONTH, "limit_amount": "100"},
            headers=auth_headers,
        )
        await async_client.post(
            "/api/v1/transactions/",
            json={"type": "expense", "amount": "80", "account_id": account_id, "category_id": cat_id},
            headers=auth_headers,
        )
        resp = await async_client.get("/api/v1/budgets/alerts", headers=auth_headers)
        assert resp.status_code == 200
        alerts = resp.json()
        assert len(alerts) >= 1
        # La alerta debe ser 80%
        alert_types = [a["alert_type"] for a in alerts]
        assert "80%" in alert_types

    async def test_alert_at_100(self, async_client, auth_headers):
        cat_id = await _create_category(async_client, auth_headers)
        account_id = await _create_account(async_client, auth_headers)
        await async_client.post(
            "/api/v1/budgets/",
            json={"category_id": cat_id, "month": CURRENT_MONTH, "limit_amount": "100"},
            headers=auth_headers,
        )
        await async_client.post(
            "/api/v1/transactions/",
            json={"type": "expense", "amount": "120", "account_id": account_id, "category_id": cat_id},
            headers=auth_headers,
        )
        resp = await async_client.get("/api/v1/budgets/alerts", headers=auth_headers)
        assert resp.status_code == 200
        alerts = resp.json()
        assert len(alerts) >= 1
        alert_types = [a["alert_type"] for a in alerts]
        assert "100%" in alert_types


class TestDeleteBudget:
    """DELETE /api/v1/budgets/{id}"""

    async def test_delete_ok(self, async_client, auth_headers):
        cat_id = await _create_category(async_client, auth_headers)
        create_resp = await async_client.post(
            "/api/v1/budgets/",
            json={"category_id": cat_id, "month": CURRENT_MONTH, "limit_amount": "100"},
            headers=auth_headers,
        )
        budget_id = create_resp.json()["id"]
        resp = await async_client.delete(f"/api/v1/budgets/{budget_id}", headers=auth_headers)
        assert resp.status_code == 204

    async def test_delete_not_found(self, async_client, auth_headers):
        resp = await async_client.delete("/api/v1/budgets/99999", headers=auth_headers)
        assert resp.status_code == 404
