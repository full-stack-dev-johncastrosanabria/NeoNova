"""Authentication service for password hashing and JWT management."""

from datetime import datetime, timedelta, timezone
from uuid import UUID

import bcrypt
from jose import ExpiredSignatureError, JWTError, jwt

from application.config import get_settings


class AuthService:
    """Service handling password hashing and JWT token operations."""

    def hash_password(self, password: str) -> str:
        """Hash a plain-text password using bcrypt.

        Args:
            password: The plain-text password to hash.

        Returns:
            The bcrypt-hashed password string.
        """
        # Truncate password to 72 bytes for bcrypt compatibility
        password_bytes = password.encode('utf-8')
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
        
        # Hash with bcrypt
        salt = bcrypt.gensalt(rounds=12)
        hashed = bcrypt.hashpw(password_bytes, salt)
        return hashed.decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain-text password against a bcrypt hash.

        Args:
            plain_password: The plain-text password provided by the user.
            hashed_password: The stored bcrypt hash to compare against.

        Returns:
            True if the password matches, False otherwise.
        """
        # Truncate password to 72 bytes for bcrypt compatibility
        password_bytes = plain_password.encode('utf-8')
        if len(password_bytes) > 72:
            password_bytes = password_bytes[:72]
        
        return bcrypt.checkpw(password_bytes, hashed_password.encode('utf-8'))

    def create_access_token(self, user_id: UUID) -> str:
        """Create a signed JWT access token for the given user.

        Args:
            user_id: The UUID of the authenticated user.

        Returns:
            A signed JWT string.
        """
        settings = get_settings()
        payload = {
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc) + timedelta(
                minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
            ),
        }
        return jwt.encode(
            payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )

    def decode_token(self, token: str) -> UUID:
        """Decode a JWT access token and return the user UUID.

        Args:
            token: The JWT string to decode.

        Returns:
            The UUID extracted from the token's "sub" claim.

        Raises:
            ValueError: If the token is expired or otherwise invalid.
        """
        settings = get_settings()
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            return UUID(payload["sub"])
        except ExpiredSignatureError as exc:
            raise ValueError("Token expired") from exc
        except JWTError as exc:
            raise ValueError("Invalid token") from exc
