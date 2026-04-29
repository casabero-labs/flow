"""Tests de autenticación — register, login, token, /me.

Cubre:
- Registro exitoso
- Email duplicado
- Login exitoso
- Credenciales inválidas
- /me con y sin token
- Token inválido / expirado
"""
import pytest
from httpx import AsyncClient


class TestRegister:
    """POST /api/v1/auth/register"""

    @pytest.mark.asyncio
    async def test_register_ok(self, async_client: AsyncClient):
        """Registro exitoso devuelve 201 y datos del usuario."""
        payload = {
            "email": "fresh@test.com",
            "password": "Secret123!",
            "name": "Fresh User",
        }
        resp = await async_client.post("/api/v1/auth/register", json=payload)
        assert resp.status_code == 201
        data = resp.json()
        assert data["email"] == "fresh@test.com"
        assert data["name"] == "Fresh User"
        assert data["is_active"] is True
        assert "id" in data

    @pytest.mark.asyncio
    async def test_register_no_password(self, async_client: AsyncClient):
        """Falta password → 422."""
        resp = await async_client.post("/api/v1/auth/register", json={
            "email": "nopass@test.com",
            "name": "No Pass",
        })
        assert resp.status_code == 422

    @pytest.mark.asyncio
    async def test_register_invalid_email(self, async_client: AsyncClient):
        """Email inválido → 422."""
        resp = await async_client.post("/api/v1/auth/register", json={
            "email": "not-an-email",
            "password": "Secret123!",
            "name": "Bad Email",
        })
        assert resp.status_code == 422

    @pytest.mark.asyncio
    async def test_register_duplicate_email(self, async_client: AsyncClient):
        """Registrar con email ya existente → 400."""
        payload = {
            "email": "dup@test.com",
            "password": "Secret123!",
            "name": "First",
        }
        resp1 = await async_client.post("/api/v1/auth/register", json=payload)
        assert resp1.status_code == 201

        resp2 = await async_client.post("/api/v1/auth/register", json=payload)
        assert resp2.status_code == 400
        assert "registrado" in resp2.json()["detail"].lower()


class TestLogin:
    """POST /api/v1/auth/login"""

    @pytest.mark.asyncio
    async def test_login_ok(self, async_client: AsyncClient):
        """Login exitoso devuelve token + user."""
        await async_client.post("/api/v1/auth/register", json={
            "email": "login@test.com",
            "password": "Pass1234!",
            "name": "Login User",
        })
        resp = await async_client.post("/api/v1/auth/login", json={
            "email": "login@test.com",
            "password": "Pass1234!",
        })
        assert resp.status_code == 200
        data = resp.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"]["email"] == "login@test.com"

    @pytest.mark.asyncio
    async def test_login_wrong_password(self, async_client: AsyncClient):
        """Contraseña incorrecta → 401."""
        await async_client.post("/api/v1/auth/register", json={
            "email": "wrong@test.com",
            "password": "Correct1!",
            "name": "Wrong Pass",
        })
        resp = await async_client.post("/api/v1/auth/login", json={
            "email": "wrong@test.com",
            "password": "WrongPass!",
        })
        assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_login_nonexistent_user(self, async_client: AsyncClient):
        """Usuario no existe → 401."""
        resp = await async_client.post("/api/v1/auth/login", json={
            "email": "ghost@test.com",
            "password": "SomePass1!",
        })
        assert resp.status_code == 401


class TestMe:
    """GET /api/v1/auth/me"""

    @pytest.mark.asyncio
    async def test_me_with_token(self, async_client: AsyncClient, auth_headers: dict):
        """/me con token válido retorna datos del usuario."""
        resp = await async_client.get("/api/v1/auth/me", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == "test@example.com"
        assert data["name"] == "Test User"

    @pytest.mark.asyncio
    async def test_me_without_token(self, async_client: AsyncClient):
        """/me sin token → 401 (HTTPBearer sin credenciales)."""
        resp = await async_client.get("/api/v1/auth/me")
        assert resp.status_code == 401

    @pytest.mark.asyncio
    async def test_me_invalid_token(self, async_client: AsyncClient):
        """/me con token basura → 401."""
        headers = {"Authorization": "Bearer este-no-es-un-token-valido"}
        resp = await async_client.get("/api/v1/auth/me", headers=headers)
        assert resp.status_code == 401
        assert "inválido" in resp.json()["detail"].lower()
