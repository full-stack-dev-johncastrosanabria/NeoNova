"""SQLAlchemy implementation of IUserRepository."""

from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.interfaces.repositories import IUserRepository
from domain.entities.user import User
from infrastructure.models.user_model import UserModel


class UserRepository(IUserRepository):
    """Concrete user repository backed by an async SQLAlchemy session."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, user: User) -> User:
        """Persist a new user and return the saved entity."""
        model = UserModel(
            id=user.id,
            email=user.email,
            display_name=user.display_name,
            password_hash=user.password_hash,
            created_at=user.created_at,
        )
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        """Return the user with the given ID, or None if not found."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def find_by_email(self, email: str) -> Optional[User]:
        """Return the user with the given email, or None if not found."""
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    def _to_entity(self, model: UserModel) -> User:
        """Convert a UserModel ORM instance to a User domain entity."""
        return User(
            id=model.id,
            email=model.email,
            display_name=model.display_name,
            password_hash=model.password_hash,
            created_at=model.created_at,
        )
