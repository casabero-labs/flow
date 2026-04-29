"""Basic tests for the Flow backend API."""

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """GET /health debería retornar status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["app"] == "flow"


def test_app_title():
    """El título de la app debe ser 'flow API'."""
    assert app.title == "flow API"
