"""
Tests de metas — CRUD + contribuciones + progreso.

Cubre:
- Crear meta
- Listar metas (vacío, con datos, progreso calculado)
- Contribuir a meta (incrementa progreso)
- Eliminar meta propia
- Meta de otro usuario
"""
import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestCreateGoal:
    """POST /api/v1/goals/"""

    async def test_create_ok(self, async_client, auth_headers):
        resp = await async_client.post(
            "/api/v1/goals/",
            json={
                "name": "Viaje a México",
                "target_amount": "5000.00",
                "emoji": "✈️",
            },
            headers=auth_headers,
        )
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Viaje a México"
        assert float(data["target_amount"]) == 5000.0
        assert data["emoji"] == "✈️"
        assert data["current_amount"] is None or float(data["current_amount"]) == 0.0

    async def test_create_with_deadline(self, async_client, auth_headers):
        resp = await async_client.post(
            "/api/v1/goals/",
            json={
                "name": "Ahorro",
                "target_amount": "1000",
                "deadline": "2025-12-31T00:00:00",
            },
            headers=auth_headers,
        )
        assert resp.status_code == 201
        assert resp.json()["deadline"] is not None


class TestListGoals:
    """GET /api/v1/goals/"""

    async def test_list_empty(self, async_client, auth_headers):
        resp = await async_client.get("/api/v1/goals/", headers=auth_headers)
        assert resp.status_code == 200
        assert resp.json() == []

    async def test_list_with_progress(self, async_client, auth_headers):
        """Al listar, las metas deben mostrar progreso calculado."""
        resp = await async_client.post(
            "/api/v1/goals/",
            json={"name": "Fondo Emergencia", "target_amount": "2000"},
            headers=auth_headers,
        )
        goal_id = resp.json()["id"]

        # Contribuir
        await async_client.post(
            f"/api/v1/goals/{goal_id}/contribute",
            json={"amount": "500", "note": "Primer aporte"},
            headers=auth_headers,
        )

        list_resp = await async_client.get("/api/v1/goals/", headers=auth_headers)
        assert list_resp.status_code == 200
        goals = list_resp.json()
        assert len(goals) == 1
        goal = goals[0]
        assert float(goal["current_amount"]) == 500.0
        assert float(goal["progress_pct"]) == 25.0  # 500/2000 = 25%


class TestContribute:
    """POST /api/v1/goals/{id}/contribute"""

    async def test_contribute_increases_progress(self, async_client, auth_headers):
        create_resp = await async_client.post(
            "/api/v1/goals/",
            json={"name": "Fondo", "target_amount": "1000"},
            headers=auth_headers,
        )
        goal_id = create_resp.json()["id"]

        # Contribuir 300
        resp1 = await async_client.post(
            f"/api/v1/goals/{goal_id}/contribute",
            json={"amount": "300.00"},
            headers=auth_headers,
        )
        assert resp1.status_code == 200
        assert float(resp1.json()["current_amount"]) == 300.0

        # Contribuir otros 200 → total 500
        resp2 = await async_client.post(
            f"/api/v1/goals/{goal_id}/contribute",
            json={"amount": "200.00", "note": "Segundo"},
            headers=auth_headers,
        )
        assert resp2.status_code == 200
        assert float(resp2.json()["current_amount"]) == 500.0
        assert float(resp2.json()["progress_pct"]) == 50.0

    async def test_contribute_goal_not_found(self, async_client, auth_headers):
        resp = await async_client.post(
            "/api/v1/goals/99999/contribute",
            json={"amount": "100"},
            headers=auth_headers,
        )
        assert resp.status_code == 404


class TestDeleteGoal:
    """DELETE /api/v1/goals/{id}"""

    async def test_delete_own(self, async_client, auth_headers):
        create_resp = await async_client.post(
            "/api/v1/goals/",
            json={"name": "Temp Goal", "target_amount": "500"},
            headers=auth_headers,
        )
        goal_id = create_resp.json()["id"]
        resp = await async_client.delete(f"/api/v1/goals/{goal_id}", headers=auth_headers)
        assert resp.status_code == 204

    async def test_delete_not_found(self, async_client, auth_headers):
        resp = await async_client.delete("/api/v1/goals/99999", headers=auth_headers)
        assert resp.status_code == 404

    async def test_delete_other_users_goal(self, async_client, auth_headers, second_user_headers):
        create_resp = await async_client.post(
            "/api/v1/goals/",
            json={"name": "Goal de Luz", "target_amount": "1000"},
            headers=second_user_headers,
        )
        goal_id = create_resp.json()["id"]
        resp = await async_client.delete(f"/api/v1/goals/{goal_id}", headers=auth_headers)
        assert resp.status_code == 404
