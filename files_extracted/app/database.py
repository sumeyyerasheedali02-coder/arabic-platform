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


async def init_db() -> None:
    """Create tables that do not exist yet. Existing tables are never altered."""
    from app import models  # noqa: F401  (registers the tables on Base.metadata)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


__all__ = ["AsyncSession", "AsyncSessionLocal", "Base", "engine", "get_db", "init_db"]
