"""Tests para el endpoint de telemetría."""
import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
class TestTelemetry:
    """Telemetry endpoint — registro de eventos."""

    async def test_create_event_anonymous(self, async_client: AsyncClient):
        """Evento anónimo (sin token) se guarda correctamente."""
        resp = await async_client.post(
            "/api/v1/telemetry/",
            json={
                "event_type": "page_view",
                "event_data": {"path": "/dashboard"},
                "session_id": "abc-123",
            },
        )
        assert resp.status_code == 201
        body = resp.json()
        assert body["status"] == "ok"
        assert "id" in body

    async def test_create_event_authenticated(self, async_client: AsyncClient, auth_headers: dict):
        """Evento autenticado asocia el user_id."""
        resp = await async_client.post(
            "/api/v1/telemetry/",
            json={
                "event_type": "button_click",
                "event_data": {"button": "save"},
            },
            headers=auth_headers,
        )
        assert resp.status_code == 201
        body = resp.json()
        assert body["status"] == "ok"

    async def test_create_event_minimal(self, async_client: AsyncClient):
        """Evento mínimo (solo event_type, sin event_data ni session_id)."""
        resp = await async_client.post(
            "/api/v1/telemetry/",
            json={"event_type": "app_open"},
        )
        assert resp.status_code == 201

    async def test_create_event_without_type_fails(self, async_client: AsyncClient):
        """Sin event_type debe dar 422."""
        resp = await async_client.post(
            "/api/v1/telemetry/",
            json={"event_data": {"something": "here"}},
        )
        assert resp.status_code == 422
