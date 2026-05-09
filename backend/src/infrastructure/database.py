"""Async SQLAlchemy engine, session factory, and base declarative class."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from application.config import get_settings


class Base(DeclarativeBase):
    """Declarative base for all SQLAlchemy ORM models."""


_engine = None
_AsyncSessionLocal = None


def get_engine():
    """Create and return an async SQLAlchemy engine from settings."""
    global _engine
    if _engine is None:
        _engine = create_async_engine(
            get_settings().DATABASE_URL,
            echo=False,
        )
    return _engine


def get_async_session_local():
    """Get or create the async session factory."""
    global _AsyncSessionLocal
    if _AsyncSessionLocal is None:
        _AsyncSessionLocal = async_sessionmaker(
            bind=get_engine(),
            class_=AsyncSession,
            expire_on_commit=False,
        )
    return _AsyncSessionLocal


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields an async database session."""
    AsyncSessionLocal = get_async_session_local()
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()
