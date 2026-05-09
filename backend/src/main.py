"""NeoNova AI Assistant — FastAPI application entry point."""

import os
import traceback
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from infrastructure.llm_providers.exceptions import (
    RateLimitError,
    ServiceUnavailableError,
)


# ---------------------------------------------------------------------------
# Lifespan
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown hooks."""
    # Startup
    yield
    # Shutdown


# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="NeoNova AI Assistant",
        description=(
            "Conversational AI assistant with memory and agent orchestration."
        ),
        version="0.1.0",
        lifespan=lifespan,
    )

    # ------------------------------------------------------------------
    # CORS middleware
    # ------------------------------------------------------------------
    raw_origins = os.getenv("CORS_ALLOW_ORIGINS", "http://localhost:5173")
    allow_origins = [o.strip() for o in raw_origins.split(",") if o.strip()]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ------------------------------------------------------------------
    # Global exception handlers
    # ------------------------------------------------------------------

    @app.exception_handler(ValueError)
    async def value_error_handler(
        request: Request, exc: ValueError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={
                "error": "Bad Request",
                "message": str(exc),
                "details": None,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

    @app.exception_handler(PermissionError)
    async def permission_error_handler(
        request: Request, exc: PermissionError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=403,
            content={
                "error": "Forbidden",
                "message": str(exc),
                "details": None,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

    @app.exception_handler(RateLimitError)
    async def rate_limit_error_handler(
        request: Request, exc: RateLimitError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=429,
            content={
                "error": "Too Many Requests",
                "message": (
                    str(exc) or "Rate limit exceeded. Please try again later."
                ),
                "details": None,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

    @app.exception_handler(ServiceUnavailableError)
    async def service_unavailable_error_handler(
        request: Request, exc: ServiceUnavailableError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=503,
            content={
                "error": "Service Unavailable",
                "message": (
                    str(exc) or "The AI service is temporarily unavailable."
                ),
                "details": None,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal Server Error",
                "message": "An unexpected error occurred.",
                "details": None,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        )

    # ------------------------------------------------------------------
    # Router registration
    # ------------------------------------------------------------------
    from api.routes.auth_routes import router as auth_router
    from api.routes.conversation_routes import router as conversation_router
    from api.routes.feedback_routes import router as feedback_router
    from api.routes.memory_routes import router as memory_router
    from api.routes.message_routes import router as message_router

    app.include_router(auth_router)
    app.include_router(conversation_router)
    app.include_router(message_router)
    app.include_router(memory_router)
    app.include_router(feedback_router)

    # ------------------------------------------------------------------
    # Health check
    # ------------------------------------------------------------------

    @app.get("/health", tags=["health"])
    async def health_check():
        return {
            "status": "ok",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
