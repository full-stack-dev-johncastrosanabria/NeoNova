"""Authentication use cases for user registration and login."""

from datetime import datetime
from uuid import uuid4

from application.dtos.auth_dtos import LoginDTO, RegisterUserDTO
from application.interfaces.repositories import IUserRepository
from application.services.auth_service import AuthService
from domain.entities.user import User


class RegisterUserUseCase:
    """Use case for registering a new user."""

    def __init__(
        self,
        user_repo: IUserRepository,
        auth_service: AuthService,
    ) -> None:
        """Initialise with required dependencies.

        Args:
            user_repo: Repository for user persistence.
            auth_service: Service for password hashing and JWT operations.
        """
        self.user_repo = user_repo
        self.auth_service = auth_service

    async def execute(self, dto: RegisterUserDTO) -> User:
        """Register a new user.

        Args:
            dto: Data transfer object containing registration details.

        Returns:
            The newly created and persisted User entity.

        Raises:
            ValueError: If the email address is already registered.
        """
        existing = await self.user_repo.find_by_email(dto.email)
        if existing:
            raise ValueError("Email already registered")

        password_hash = self.auth_service.hash_password(dto.password)

        user = User(
            id=uuid4(),
            email=dto.email,
            display_name=dto.display_name,
            password_hash=password_hash,
            created_at=datetime.utcnow(),
        )

        return await self.user_repo.create(user)


class LoginUseCase:
    """Use case for authenticating an existing user."""

    def __init__(
        self,
        user_repo: IUserRepository,
        auth_service: AuthService,
    ) -> None:
        """Initialise with required dependencies.

        Args:
            user_repo: Repository for user persistence.
            auth_service: Service for password verification and JWT creation.
        """
        self.user_repo = user_repo
        self.auth_service = auth_service

    async def execute(self, dto: LoginDTO) -> tuple[str, User]:
        """Authenticate a user and return an access token.

        Args:
            dto: Data transfer object containing login credentials.

        Returns:
            A tuple of (access_token, user) on successful authentication.

        Raises:
            ValueError: If the email is not found or the password is wrong.
        """
        user = await self.user_repo.find_by_email(dto.email)
        if not user:
            raise ValueError("Invalid credentials")

        if not self.auth_service.verify_password(
            dto.password, user.password_hash
        ):
            raise ValueError("Invalid credentials")

        token = self.auth_service.create_access_token(user.id)
        return token, user
