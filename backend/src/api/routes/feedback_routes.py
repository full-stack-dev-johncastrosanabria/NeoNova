"""FastAPI route handlers for feedback endpoints."""

from fastapi import APIRouter, Depends, HTTPException

from api.auth import get_current_user
from api.dependencies import get_create_feedback_use_case
from api.schemas.feedback_schemas import FeedbackRequest, FeedbackResponse
from application.dtos.feedback_dtos import CreateFeedbackDTO
from application.use_cases.feedback_use_cases import CreateFeedbackUseCase
from domain.entities.user import User

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("/", status_code=201, response_model=FeedbackResponse)
async def create_feedback(
    body: FeedbackRequest,
    current_user: User = Depends(get_current_user),
    use_case: CreateFeedbackUseCase = Depends(get_create_feedback_use_case),
) -> FeedbackResponse:
    """Submit feedback for an assistant message.

    Args:
        body: Request body containing message_id, rating, comment, and
            optional correction.
        current_user: The authenticated user from the JWT token.
        use_case: Injected use case for feedback creation.

    Returns:
        201 FeedbackResponse on success.

    Raises:
        HTTPException 404: If the target message is not found.
        HTTPException 409: If feedback already exists for the message.
    """
    try:
        feedback = await use_case.execute(
            dto=CreateFeedbackDTO(
                message_id=body.message_id,
                rating=body.rating,
                comment=body.comment,
                correction=body.correction,
            ),
            user_id=current_user.id,
        )
    except ValueError as exc:
        error_msg = str(exc).lower()
        if "not found" in error_msg:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        if "already exists" in error_msg:
            raise HTTPException(status_code=409, detail=str(exc)) from exc
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return FeedbackResponse(
        id=feedback.id,
        message_id=feedback.message_id,
        rating=feedback.rating,
        comment=feedback.comment,
        correction=feedback.correction,
        created_at=feedback.created_at,
    )
