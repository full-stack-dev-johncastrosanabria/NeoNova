"""Integration tests for authentication flow."""

import pytest
from httpx import AsyncClient


class TestAuthenticationFlow:
    """Test suite for user registration and login flows."""

    # -----------------------------------------------------------------------
    # Registration Tests
    # -----------------------------------------------------------------------

    @pytest.mark.asyncio
    async def test_register_with_valid_data(self, test_client: AsyncClient):
        """Test: POST /auth/register with valid data → 201, user returned, password_hash not in response."""
        response = await test_client.post(
            "/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "securepassword123",
                "display_name": "New User",
            },
        )

        assert response.status_code == 201
        data = response.json()

        # Verify user data is returned
        assert "id" in data
        assert data["email"] == "newuser@example.com"
        assert data["display_name"] == "New User"
        assert "created_at" in data

        # Verify password_hash is NOT in response
        assert "password_hash" not in data
        assert "password" not in data

    @pytest.mark.asyncio
    async def test_register_with_duplicate_email(
        self, test_client: AsyncClient, test_user
    ):
        """Test: POST /auth/register with duplicate email → 400 error."""
        response = await test_client.post(
            "/auth/register",
            json={
                "email": test_user.email,  # Use existing user's email
                "password": "anotherpassword123",
                "display_name": "Another User",
            },
        )

        assert response.status_code == 400
        data = response.json()
        assert "message" in data or "detail" in data

    @pytest.mark.asyncio
    async def test_register_with_invalid_email_format(self, test_client: AsyncClient):
        """Test: POST /auth/register with invalid email format → 422 validation error."""
        response = await test_client.post(
            "/auth/register",
            json={
                "email": "not-an-email",  # Invalid email format
                "password": "securepassword123",
                "display_name": "New User",
            },
        )

        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    @pytest.mark.asyncio
    async def test_register_with_password_too_short(self, test_client: AsyncClient):
        """Test: POST /auth/register with password < 8 chars → 422 validation error."""
        response = await test_client.post(
            "/auth/register",
            json={
                "email": "newuser@example.com",
                "password": "short",  # Less than 8 characters
                "display_name": "New User",
            },
        )

        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

    # -----------------------------------------------------------------------
    # Login Tests
    # -----------------------------------------------------------------------

    @pytest.mark.asyncio
    async def test_login_with_correct_credentials(
        self, test_client: AsyncClient, test_user
    ):
        """Test: POST /auth/login with correct credentials → 200, token returned."""
        response = await test_client.post(
            "/auth/login",
            json={
                "email": test_user.email,
                "password": "password123",  # Matches the test_user fixture
            },
        )

        assert response.status_code == 200
        data = response.json()

        # Verify token is returned
        assert "token" in data
        assert isinstance(data["token"], str)
        assert len(data["token"]) > 0

        # Verify user data is returned
        assert "user" in data
        assert data["user"]["email"] == test_user.email
        assert data["user"]["display_name"] == test_user.display_name
        assert "id" in data["user"]

        # Verify password_hash is NOT in response
        assert "password_hash" not in data["user"]
        assert "password" not in data["user"]

    @pytest.mark.asyncio
    async def test_login_with_wrong_password(
        self, test_client: AsyncClient, test_user
    ):
        """Test: POST /auth/login with wrong password → 401 error."""
        response = await test_client.post(
            "/auth/login",
            json={
                "email": test_user.email,
                "password": "wrongpassword",  # Incorrect password
            },
        )

        assert response.status_code == 401
        data = response.json()
        assert "message" in data or "detail" in data

    @pytest.mark.asyncio
    async def test_login_with_non_existent_email(self, test_client: AsyncClient):
        """Test: POST /auth/login with non-existent email → 401 error."""
        response = await test_client.post(
            "/auth/login",
            json={
                "email": "nonexistent@example.com",
                "password": "somepassword123",
            },
        )

        assert response.status_code == 401
        data = response.json()
        assert "message" in data or "detail" in data

    # -----------------------------------------------------------------------
    # Protected Endpoint Tests
    # -----------------------------------------------------------------------

    @pytest.mark.asyncio
    async def test_protected_endpoint_with_valid_token(
        self, test_client: AsyncClient, test_user_token
    ):
        """Test: Accessing a protected endpoint with valid token → 200."""
        # Use the /memories endpoint as a protected endpoint
        response = await test_client.get(
            "/memories/",
            headers={"Authorization": f"Bearer {test_user_token}"},
        )

        # Should succeed (200 or 204 depending on implementation)
        assert response.status_code in [200, 204]

    @pytest.mark.asyncio
    async def test_protected_endpoint_with_expired_token(
        self, test_client: AsyncClient
    ):
        """Test: Accessing a protected endpoint with expired token → 401."""
        # Create an expired token by manipulating the expiry
        from application.services.auth_service import AuthService
        from datetime import datetime, timedelta, timezone
        from jose import jwt
        from application.config import get_settings
        from uuid import uuid4

        settings = get_settings()
        user_id = uuid4()

        # Create a token that's already expired
        payload = {
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc) - timedelta(hours=1),  # Expired
        }
        expired_token = jwt.encode(
            payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM
        )

        response = await test_client.get(
            "/memories/",
            headers={"Authorization": f"Bearer {expired_token}"},
        )

        assert response.status_code == 401
        data = response.json()
        assert "message" in data or "detail" in data

    @pytest.mark.asyncio
    async def test_protected_endpoint_with_invalid_token(
        self, test_client: AsyncClient
    ):
        """Test: Accessing a protected endpoint with invalid token → 401."""
        response = await test_client.get(
            "/memories/",
            headers={"Authorization": "Bearer invalid.token.here"},
        )

        assert response.status_code == 401
        data = response.json()
        assert "message" in data or "detail" in data

    @pytest.mark.asyncio
    async def test_protected_endpoint_without_token(self, test_client: AsyncClient):
        """Test: Accessing a protected endpoint without token → 401."""
        response = await test_client.get("/memories/")

        assert response.status_code == 401  # HTTPBearer returns 401 when no credentials
