"""FastAPI route handlers for authentication endpoints."""

from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import get_login_use_case, get_register_use_case
from api.schemas.auth_schemas import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    UserResponse,
)
from application.dtos.auth_dtos import LoginDTO, RegisterUserDTO
from application.use_cases.auth_use_cases import (
    LoginUseCase,
    RegisterUserUseCase,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=201, response_model=UserResponse)
async def register(
    body: RegisterRequest,
    register_use_case: RegisterUserUseCase = Depends(get_register_use_case),
) -> UserResponse:
    """Register a new user account.

    Args:
        body: Registration request containing email, password, display_name.
        register_use_case: Injected use case for user registration.

    Returns:
        201 UserResponse on success.

    Raises:
        HTTPException 400: If the email is already registered or input is
            invalid.
    """
    try:
        user = await register_use_case.execute(
            RegisterUserDTO(
                email=body.email,
                password=body.password,
                display_name=body.display_name,
            )
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return UserResponse(
        id=user.id,
        email=user.email,
        display_name=user.display_name,
        created_at=user.created_at,
    )


@router.post("/login", status_code=200, response_model=LoginResponse)
async def login(
    body: LoginRequest,
    login_use_case: LoginUseCase = Depends(get_login_use_case),
) -> LoginResponse:
    """Authenticate a user and return an access token.

    Args:
        body: Login request containing email and password.
        login_use_case: Injected use case for user login.

    Returns:
        200 LoginResponse with JWT token and user details.

    Raises:
        HTTPException 401: If credentials are invalid.
    """
    try:
        token, user = await login_use_case.execute(
            LoginDTO(email=body.email, password=body.password)
        )
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc

    return LoginResponse(
        token=token,
        user=UserResponse(
            id=user.id,
            email=user.email,
            display_name=user.display_name,
            created_at=user.created_at,
        ),
    )
