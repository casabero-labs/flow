"""
Fixtures para tests del backend Flow.

SQLite en memoria (:memory:) — NO toca flow.db real.
Usa dependency_overrides de FastAPI para inyectar la sesión de test.
"""
import asyncio
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.database import Base, get_db
from app.main import app
from app.config import settings

# ── Engine de test (SQLite en memoria) ──────────────────────────
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
)

TestSessionLocal = async_sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    """Crea un event loop para toda la sesión de tests."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest_asyncio.fixture(autouse=True)
async def setup_database():
    """Crea tablas antes de cada test y las dropea después.
    
    SQLite en memoria se reinicia en cada sesión, pero dropear/crear
    asegura un estado limpio entre tests.
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def _get_test_db() -> AsyncGenerator[AsyncSession, None]:
    """Generador de sesión de test para dependency_overrides."""
    async with TestSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Fixture directo para operaciones con la BD en tests."""
    async with TestSessionLocal() as session:
        yield session


@pytest_asyncio.fixture
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Cliente HTTP async con dependency_overrides para usar BD en memoria.
    
    Uso:
        response = await async_client.get("/api/v1/auth/me")
    """
    app.dependency_overrides[get_db] = _get_test_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def auth_headers(async_client: AsyncClient) -> dict[str, str]:
    """
    Registra un usuario de test y retorna headers con Bearer token.
    
    Uso:
        headers = await auth_headers  # dict con Authorization: Bearer <token>
        response = await async_client.get("/api/v1/auth/me", headers=headers)
    """
    register_payload = {
        "email": "test@example.com",
        "password": "SecurePass123!",
        "name": "Test User",
    }
    resp = await async_client.post("/api/v1/auth/register", json=register_payload)
    assert resp.status_code == 201, f"Error registrando usuario test: {resp.text}"

    login_resp = await async_client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "SecurePass123!",
    })
    assert login_resp.status_code == 200, f"Error login test: {login_resp.text}"
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def second_user_headers(async_client: AsyncClient) -> dict[str, str]:
    """
    Registra un segundo usuario (útil para tests de partnership y permisos).
    """
    register_payload = {
        "email": "luz@example.com",
        "password": "LuzPass456!",
        "name": "Luz",
    }
    resp = await async_client.post("/api/v1/auth/register", json=register_payload)
    assert resp.status_code == 201

    login_resp = await async_client.post("/api/v1/auth/login", json={
        "email": "luz@example.com",
        "password": "LuzPass456!",
    })
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
