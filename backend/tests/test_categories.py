"""
Tests de categorías — CRUD + defaults al registrar usuario.

Cubre:
- Listar categorías vacío → se crean defaults automáticamente
- Crear categoría personalizada
- Eliminar categoría propia
- No se puede eliminar categoría default
- No se puede eliminar categoría de otro usuario
- Sin autenticación
"""
import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestListCategories:
    """GET /api/v1/categories/"""

    async def test_list_creates_defaults_on_empty(self, async_client, auth_headers):
        """Si no hay categorías, se crean las defaults al listar."""
        resp = await async_client.get("/api/v1/categories/", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert len(data) > 0
        # Deberían incluir categorías default como Comida, Transporte, etc.
        names = [c["name"] for c in data]
        assert "Comida" in names
        assert "Otros" in names

    async def test_list_without_auth(self, async_client):
        resp = await async_client.get("/api/v1/categories/")
        assert resp.status_code == 401


class TestCreateCategory:
    """POST /api/v1/categories/"""

    async def test_create_ok(self, async_client, auth_headers):
        resp = await async_client.post(
            "/api/v1/categories/",
            json={"name": "Mascotas", "icon": "🐶", "color": "#FF5733"},
            headers=auth_headers,
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Mascotas"
        assert data["icon"] == "🐶"
        assert data["is_default"] is False
        assert data["user_id"] is not None

    async def test_create_minimal(self, async_client, auth_headers):
        resp = await async_client.post(
            "/api/v1/categories/",
            json={"name": "Minimal"},
            headers=auth_headers,
        )
        assert resp.status_code == 201
        assert resp.json()["icon"] == "💰"  # default
        assert resp.json()["color"] == "#6B7280"  # default


class TestDeleteCategory:
    """DELETE /api/v1/categories/{id}"""

    async def test_delete_own_category(self, async_client, auth_headers):
        # Crear categoría
        create_resp = await async_client.post(
            "/api/v1/categories/",
            json={"name": "Borrable"},
            headers=auth_headers,
        )
        cat_id = create_resp.json()["id"]
        resp = await async_client.delete(f"/api/v1/categories/{cat_id}", headers=auth_headers)
        assert resp.status_code == 204

    async def test_delete_default_category_fails(self, async_client, auth_headers):
        """Las categorías default no se pueden borrar."""
        # Primero listar para obtener defaults
        list_resp = await async_client.get("/api/v1/categories/", headers=auth_headers)
        defaults = [c for c in list_resp.json() if c["is_default"]]
        assert len(defaults) > 0
        default_id = defaults[0]["id"]
        resp = await async_client.delete(f"/api/v1/categories/{default_id}", headers=auth_headers)
        assert resp.status_code == 400
        assert "default" in resp.json()["detail"].lower()

    async def test_delete_nonexistent(self, async_client, auth_headers):
        resp = await async_client.delete("/api/v1/categories/99999", headers=auth_headers)
        assert resp.status_code == 404

    async def test_delete_other_users_category(self, async_client, auth_headers, second_user_headers):
        """No se puede borrar categoría creada por otro usuario."""
        create_resp = await async_client.post(
            "/api/v1/categories/",
            json={"name": "De Luz"},
            headers=second_user_headers,
        )
        cat_id = create_resp.json()["id"]
        resp = await async_client.delete(f"/api/v1/categories/{cat_id}", headers=auth_headers)
        assert resp.status_code == 403
