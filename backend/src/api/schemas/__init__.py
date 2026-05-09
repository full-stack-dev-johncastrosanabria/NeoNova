"""API schemas package — exports all Pydantic request/response models."""

from api.schemas.auth_schemas import (
    LoginRequest,
    LoginResponse,
    RegisterRequest,
    UserResponse,
)
from api.schemas.conversation_schemas import (
    ConversationRequest,
    ConversationResponse,
    MessageRequest,
    MessageResponse,
)
from api.schemas.error_schemas import ErrorResponse
from api.schemas.feedback_schemas import FeedbackRequest, FeedbackResponse
from api.schemas.memory_schemas import MemoryRequest, MemoryResponse

__all__ = [
    # Auth
    "RegisterRequest",
    "LoginRequest",
    "UserResponse",
    "LoginResponse",
    # Conversations & Messages
    "ConversationRequest",
    "ConversationResponse",
    "MessageRequest",
    "MessageResponse",
    # Memory
    "MemoryRequest",
    "MemoryResponse",
    # Feedback
    "FeedbackRequest",
    "FeedbackResponse",
    # Errors
    "ErrorResponse",
]
