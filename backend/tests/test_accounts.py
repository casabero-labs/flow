"""
Tests de cuentas — CRUD.

Cubre:
- Crear cuenta (cash, bank, digital)
- Listar cuentas
- Eliminar cuenta propia
- Eliminar cuenta de otro usuario
- Sin autenticación
"""
import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestCreateAccount:
    """POST /api/v1/accounts/"""

    async def test_create_cash(self, async_client, auth_headers):
        resp = await async_client.post(
            "/api/v1/accounts/",
            json={"name": "Efectivo", "account_type": "cash", "currency": "COP"},
            headers=auth_headers,
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Efectivo"
        assert data["account_type"] == "cash"
        assert data["currency"] == "COP"
        assert data["is_shared"] is False

    async def test_create_bank(self, async_client, auth_headers):
        resp = await async_client.post(
            "/api/v1/accounts/",
            json={"name": "Bancolombia", "account_type": "bank", "currency": "COP", "is_shared": True},
            headers=auth_headers,
        )
        assert resp.status_code == 201
        assert resp.json()["is_shared"] is True

    async def test_create_without_auth(self, async_client):
        resp = await async_client.post(
            "/api/v1/accounts/",
            json={"name": "Nequi", "account_type": "digital"},
        )
        assert resp.status_code == 401


class TestListAccounts:
    """GET /api/v1/accounts/"""

    async def test_list_empty(self, async_client, auth_headers):
        resp = await async_client.get("/api/v1/accounts/", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json() == []

    async def test_list_with_data(self, async_client, auth_headers):
        await async_client.post(
            "/api/v1/accounts/",
            json={"name": "Efectivo", "account_type": "cash"},
            headers=auth_headers,
        )
        await async_client.post(
            "/api/v1/accounts/",
            json={"name": "Nequi", "account_type": "digital"},
            headers=auth_headers,
        )
        resp = await async_client.get("/api/v1/accounts/", headers=auth_headers)
        assert resp.status_code == 200
        assert len(resp.json()) == 2


class TestDeleteAccount:
    """DELETE /api/v1/accounts/{id}"""

    async def test_delete_own(self, async_client, auth_headers):
        create_resp = await async_client.post(
            "/api/v1/accounts/",
            json={"name": "Temp", "account_type": "cash"},
            headers=auth_headers,
        )
        acc_id = create_resp.json()["id"]
        resp = await async_client.delete(f"/api/v1/accounts/{acc_id}", headers=auth_headers)
        assert resp.status_code == 204

    async def test_delete_not_found(self, async_client, auth_headers):
        resp = await async_client.delete("/api/v1/accounts/99999", headers=auth_headers)
        assert resp.status_code == 404

    async def test_delete_other_users_account(self, async_client, auth_headers, second_user_headers):
        create_resp = await async_client.post(
            "/api/v1/accounts/",
            json={"name": "De Luz", "account_type": "bank"},
            headers=second_user_headers,
        )
        acc_id = create_resp.json()["id"]
        resp = await async_client.delete(f"/api/v1/accounts/{acc_id}", headers=auth_headers)
        assert resp.status_code == 404  # No la ve, no existe para él
