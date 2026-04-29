"""SQLite async connection with Flow db."""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


class Base(DeclarativeBase):
    pass


# Import models to register them with Base (after Base definition to avoid circular imports)
from app.models.user import User  # noqa: F401, E402
from app.models.partnership import Partnership  # noqa: F401, E402
from app.models.account import Account  # noqa: F401, E402
from app.models.category import Category  # noqa: F401, E402
from app.models.transaction import Transaction  # noqa: F401, E402
from app.models.budget import Budget  # noqa: F401, E402
from app.models.goal import Goal  # noqa: F401, E402
from app.models.goal_contribution import GoalContribution  # noqa: F401, E402
from app.models.insight import Insight  # noqa: F401, E402
from app.models.telemetry import TelemetryEvent  # noqa: F401, E402

engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,
    pool_pre_ping=True,
)

async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """Crea todas las tablas."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
