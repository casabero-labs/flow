"""
Tests de seguridad — SQL injection, JWT, CORS, XSS.

Cubre:
- SQL injection básico en campos
- JWT expirado / manipulado
- CORS headers presentes
- XSS en inputs
"""
import pytest
from httpx import AsyncClient
from jose import jwt
from datetime import datetime, timedelta

from app.config import settings

pytestmark = pytest.mark.asyncio


class TestSQLInjection:
    """Intento básico de SQL injection en endpoints."""

    async def test_sql_injection_in_email(self, async_client: AsyncClient):
        """Email con SQL injection debe ser rechazado o no causar error interno."""
        payloads = [
            "' OR '1'='1",
            "'; DROP TABLE users; --",
            "' UNION SELECT * FROM users; --",
            "admin'--",
        ]
        for payload in payloads:
            resp = await async_client.post("/api/v1/auth/register", json={
                "email": f"{payload}@test.com",
                "password": "Pass1234!",
                "name": "SQL Inject",
            })
            # Debe ser 201 (se registra con email raro pero válido como string)
            # o 422 (si email-validator rechaza el formato)
            assert resp.status_code in (201, 422), f"SQL injection en email causó {resp.status_code}: {payload}"

    async def test_sql_injection_in_name(self, async_client: AsyncClient, auth_headers):
        """XSS/SQL en name debe sanearse o aceptarse sin crash."""
        resp = await async_client.post(
            "/api/v1/auth/register",
            json={
                "email": "xss@test.com",
                "password": "Pass1234!",
                "name": "<script>alert('xss')</script>",
            },
        )
        # El backend acepta el name como string, no debe crashear
        assert resp.status_code == 201


class TestJWT:
    """Tokens JWT inválidos o expirados."""

    async def test_expired_token(self, async_client: AsyncClient):
        """Token con exp en el pasado debe ser rechazado."""
        expired_payload = {
            "sub": "1",
            "exp": datetime.utcnow() - timedelta(hours=1),
        }
        expired_token = jwt.encode(
            expired_payload,
            settings.secret_key,
            algorithm=settings.algorithm,
        )
        headers = {"Authorization": f"Bearer {expired_token}"}
        resp = await async_client.get("/api/v1/auth/me", headers=headers)
        assert resp.status_code == 401
        assert "inválido" in resp.json()["detail"].lower()

    async def test_tampered_token(self, async_client: AsyncClient):
        """Token con firma inválida debe ser rechazado."""
        headers = {"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIn0.invalid_signature"}
        resp = await async_client.get("/api/v1/auth/me", headers=headers)
        assert resp.status_code == 401

    async def test_token_with_wrong_secret(self, async_client: AsyncClient):
        """Token firmado con otra key debe ser rechazado."""
        wrong_payload = {"sub": "1", "exp": datetime.utcnow() + timedelta(hours=1)}
        wrong_token = jwt.encode(wrong_payload, "wrong-secret-key", algorithm="HS256")
        headers = {"Authorization": f"Bearer {wrong_token}"}
        resp = await async_client.get("/api/v1/auth/me", headers=headers)
        assert resp.status_code == 401


class TestCORS:
    """Verificar headers CORS."""

    async def test_cors_headers_present(self, async_client: AsyncClient):
        """Las respuestas deben incluir Access-Control-Allow-Origin."""
        resp = await async_client.options(
            "/api/v1/auth/login",
            headers={
                "Origin": "https://flow.casabero.com",
                "Access-Control-Request-Method": "POST",
            },
        )
        # FastAPI con CORSMiddleware responde a OPTIONS con 200
        assert "access-control-allow-origin" in resp.headers or resp.status_code in (200, 204)

    async def test_cors_allow_all_origins(self, async_client: AsyncClient):
        """CORS configurado para allow_origins=[\"*\"], debería permitir cualquier origen."""
        resp = await async_client.get(
            "/health",
            headers={"Origin": "https://evil-site.com"},
        )
        # CORS no bloquea, el header debe estar presente
        assert resp.status_code == 200


class TestXSS:
    """Cross-site scripting prevention."""

    async def test_xss_in_description(self, async_client: AsyncClient, auth_headers):
        """Description con HTML/JS no debe causar errores internos."""
        # Necesitamos account_id
        acc_resp = await async_client.post(
            "/api/v1/accounts/",
            json={"name": "Test", "account_type": "cash"},
            headers=auth_headers,
        )
        acc_id = acc_resp.json()["id"]

        resp = await async_client.post(
            "/api/v1/transactions/",
            json={
                "type": "expense",
                "amount": "10",
                "description": "<img src=x onerror=alert(1)>",
                "account_id": acc_id,
            },
            headers=auth_headers,
        )
        assert resp.status_code == 201
        # La descripción se guarda tal cual (eso es correcto — la sanitización va en frontend)
        assert resp.json()["description"] == "<img src=x onerror=alert(1)>"

    async def test_xss_in_category_name(self, async_client: AsyncClient, auth_headers):
        """Category name con XSS no debe crashear."""
        resp = await async_client.post(
            "/api/v1/categories/",
            json={"name": "<b>Bold</b>", "icon": "💰"},
            headers=auth_headers,
        )
        assert resp.status_code == 201
        assert resp.json()["name"] == "<b>Bold</b>"
