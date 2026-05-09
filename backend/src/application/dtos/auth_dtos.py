"""Authentication Data Transfer Objects."""

from dataclasses import dataclass


@dataclass
class RegisterUserDTO:
    """DTO for user registration."""

    email: str
    password: str
    display_name: str


@dataclass
class LoginDTO:
    """DTO for user login."""

    email: str
    password: str
