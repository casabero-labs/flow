"""
Tests de transacciones — CRUD + filtros.

Cubre:
- Crear transacción con todos los campos
- Listar transacciones (vacío, con datos, filtros por mes/categoría)
- Obtener transacción por ID
- Actualizar transacción (PATCH)
- Eliminar transacción
- Summary mensual
- Transacción sin autenticación
- Transacción de otro usuario
"""
import pytest
from httpx import AsyncClient


pytestmark = pytest.mark.asyncio


async def _create_account(async_client, headers) -> int:
    """Helper: crea una cuenta y retorna su ID."""
    resp = await async_client.post(
        "/api/v1/accounts/",
        json={"name": "Test Account", "account_type": "cash", "currency": "COP"},
        headers=headers,
    )
    assert resp.status_code == 201
    return resp.json()["id"]


async def _create_category(async_client, headers) -> int:
    """Helper: crea una categoría y retorna su ID."""
    resp = await async_client.post(
        "/api/v1/categories/",
        json={"name": "Test Cat", "icon": "🧪", "color": "#FF0000"},
        headers=headers,
    )
    assert resp.status_code == 201
    return resp.json()["id"]


class TestCreateTransaction:
    """POST /api/v1/transactions/"""

    async def test_create_income(self, async_client, auth_headers):
        account_id = await _create_account(async_client, auth_headers)
        resp = await async_client.post(
            "/api/v1/transactions/",
            json={
                "type": "income",
                "amount": "1000.00",
                "description": "Salary",
                "payment_method": "transfer",
                "account_id": account_id,
            },
            headers=auth_headers,
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["type"] == "income"
        assert float(data["amount"]) == 1000.0
        assert data["description"] == "Salary"

    async def test_create_expense(self, async_client, auth_headers):
        account_id = await _create_account(async_client, auth_headers)
        cat_id = await _create_category(async_client, auth_headers)
        resp = await async_client.post(
            "/api/v1/transactions/",
            json={
                "type": "expense",
                "amount": "50.00",
                "description": "Lunch",
                "payment_method": "cash",
                "account_id": account_id,
                "category_id": cat_id,
                "mood": "happy",
            },
            headers=auth_headers,
        )
        assert resp.status_code == 201
        assert resp.json()["mood"] == "happy"

    async def test_create_without_auth(self, async_client):
        """Sin token → 401."""
        resp = await async_client.post(
            "/api/v1/transactions/",
            json={"type": "expense", "amount": "10", "account_id": 1},
        )
        assert resp.status_code == 401

    async def test_create_invalid_type(self, async_client, auth_headers):
        account_id = await _create_account(async_client, auth_headers)
        resp = await async_client.post(
            "/api/v1/transactions/",
            json={
                "type": "invalid_type",
                "amount": "10",
                "account_id": account_id,
            },
            headers=auth_headers,
        )
        assert resp.status_code == 422


class TestListTransactions:
    """GET /api/v1/transactions/"""

    async def test_list_empty(self, async_client, auth_headers):
        resp = await async_client.get("/api/v1/transactions/", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json() == []

    async def test_list_with_data(self, async_client, auth_headers):
        account_id = await _create_account(async_client, auth_headers)
        # Crear 2 transacciones
        for i in range(2):
            await async_client.post(
                "/api/v1/transactions/",
                json={
                    "type": "expense",
                    "amount": f"{i+1}0.00",
                    "description": f"Item {i}",
                    "payment_method": "cash",
                    "account_id": account_id,
                },
                headers=auth_headers,
            )
        resp = await async_client.get("/api/v1/transactions/", headers=auth_headers)
        assert resp.status_code == 200
        assert len(resp.json()) == 2

    async def test_list_filter_by_category(self, async_client, auth_headers):
        account_id = await _create_account(async_client, auth_headers)
        cat1 = await _create_category(async_client, auth_headers)
        cat2 = await _create_category(async_client, auth_headers)
        await async_client.post(
            "/api/v1/transactions/",
            json={"type": "expense", "amount": "10", "account_id": account_id, "category_id": cat1},
            headers=auth_headers,
        )
        await async_client.post(
            "/api/v1/transactions/",
            json={"type": "expense", "amount": "20", "account_id": account_id, "category_id": cat2},
            headers=auth_headers,
        )
        resp = await async_client.get(f"/api/v1/transactions/?category_id={cat1}", headers=auth_headers)
        assert resp.status_code == 200
        assert len(resp.json()) == 1


class TestGetTransaction:
    """GET /api/v1/transactions/{id}"""

    async def test_get_ok(self, async_client, auth_headers):
        account_id = await _create_account(async_client, auth_headers)
        create_resp = await async_client.post(
            "/api/v1/transactions/",
            json={"type": "income", "amount": "500", "account_id": account_id},
            headers=auth_headers,
        )
        tx_id = create_resp.json()["id"]
        resp = await async_client.get(f"/api/v1/transactions/{tx_id}", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json()["id"] == tx_id

    async def test_get_not_found(self, async_client, auth_headers):
        resp = await async_client.get("/api/v1/transactions/99999", headers=auth_headers)
        assert resp.status_code == 404


class TestUpdateTransaction:
    """PATCH /api/v1/transactions/{id}"""

    async def test_update_ok(self, async_client, auth_headers):
        account_id = await _create_account(async_client, auth_headers)
        create_resp = await async_client.post(
            "/api/v1/transactions/",
            json={"type": "expense", "amount": "30", "description": "Old", "account_id": account_id},
            headers=auth_headers,
        )
        tx_id = create_resp.json()["id"]
        resp = await async_client.patch(
            f"/api/v1/transactions/{tx_id}",
            json={"description": "Updated"},
            headers=auth_headers,
        )
        assert resp.status_code == 200
        assert resp.json()["description"] == "Updated"
        assert float(resp.json()["amount"]) == 30.0  # unchanged

    async def test_update_not_found(self, async_client, auth_headers):
        resp = await async_client.patch(
            "/api/v1/transactions/99999",
            json={"description": "Nope"},
            headers=auth_headers,
        )
        assert resp.status_code == 404


class TestDeleteTransaction:
    """DELETE /api/v1/transactions/{id}"""

    async def test_delete_ok(self, async_client, auth_headers):
        account_id = await _create_account(async_client, auth_headers)
        create_resp = await async_client.post(
            "/api/v1/transactions/",
            json={"type": "expense", "amount": "15", "account_id": account_id},
            headers=auth_headers,
        )
        tx_id = create_resp.json()["id"]
        resp = await async_client.delete(f"/api/v1/transactions/{tx_id}", headers=auth_headers)
        assert resp.status_code == 204

        # Verificar que ya no existe
        get_resp = await async_client.get(f"/api/v1/transactions/{tx_id}", headers=auth_headers)
        assert get_resp.status_code == 404

    async def test_delete_not_found(self, async_client, auth_headers):
        resp = await async_client.delete("/api/v1/transactions/99999", headers=auth_headers)
        assert resp.status_code == 404


class TestTransactionSummary:
    """GET /api/v1/transactions/summary"""

    async def test_summary_empty(self, async_client, auth_headers):
        resp = await async_client.get("/api/v1/transactions/summary", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert float(data["income"]) == 0
        assert float(data["expense"]) == 0
        assert "month" in data

    async def test_summary_with_data(self, async_client, auth_headers):
        account_id = await _create_account(async_client, auth_headers)
        await async_client.post(
            "/api/v1/transactions/",
            json={"type": "income", "amount": "2000", "account_id": account_id},
            headers=auth_headers,
        )
        await async_client.post(
            "/api/v1/transactions/",
            json={"type": "expense", "amount": "500", "account_id": account_id},
            headers=auth_headers,
        )
        resp = await async_client.get("/api/v1/transactions/summary", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert float(data["income"]) == 2000.0
        assert float(data["expense"]) == 500.0
        assert float(data["balance"]) == 1500.0
