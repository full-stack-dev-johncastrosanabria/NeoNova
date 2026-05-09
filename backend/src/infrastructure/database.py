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


def get_engine():
    """Create and return an async SQLAlchemy engine from settings."""
    return create_async_engine(
        get_settings().DATABASE_URL,
        echo=False,
    )


AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=get_engine(),
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields an async database session."""
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        await session.close()
