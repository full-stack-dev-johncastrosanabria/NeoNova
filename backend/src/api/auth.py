"""FastAPI dependency for extracting and validating the current user."""

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from application.services.auth_service import AuthService
from domain.entities.user import User
from infrastructure.database import get_db
from infrastructure.repositories.user_repository import UserRepository
from sqlalchemy.ext.asyncio import AsyncSession


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    db: AsyncSession = Depends(get_db),
) -> User:
    """FastAPI dependency that validates a Bearer JWT and returns the user.

    Extracts the token from the ``Authorization: Bearer <token>`` header,
    decodes it via :class:`AuthService`, then fetches the corresponding user
    from the database.

    Args:
        credentials: HTTP Bearer credentials injected by FastAPI.
        db: Async database session injected by FastAPI.

    Returns:
        The authenticated :class:`User` domain entity.

    Raises:
        HTTPException: 401 if the token is invalid, expired, or the user
            cannot be found.
    """
    token = credentials.credentials
    try:
        user_id = AuthService().decode_token(token)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc

    user = await UserRepository(db).find_by_id(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
