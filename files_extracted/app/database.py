"""Database engine and session management (the only place that creates them)."""
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings

engine = create_async_engine(get_settings().database_url, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_db():
    """FastAPI dependency: one session per request."""
    async with AsyncSessionLocal() as session:
        yield session


async def init_db() -> list[str]:
    """Bring the database to the current schema; returns the migrations applied.

    Missing tables are created, then pending migrations (changes to tables
    that already existed) are applied. Nothing is ever dropped.
    """
    from app import models  # noqa: F401  (registers the tables on Base.metadata)
    from app.legacy_schema import align_legacy_sections
    from app.migrations import apply_migrations
    from app.tracking import models as tracking_models  # noqa: F401

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await align_legacy_sections(conn)
        return await apply_migrations(conn)


__all__ = ["AsyncSession", "AsyncSessionLocal", "Base", "engine", "get_db", "init_db"]
