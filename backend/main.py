from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from config import settings
from routes import router as generations_router
from workers.async_worker import worker
from core.database import sessionmanager


# Enable remote debugging if configured
if settings.ENABLE_DEBUG:
    try:
        import debugpy
        debugpy.listen(("0.0.0.0", settings.DEBUG_PORT))
        print(f"🐛 Debugpy listening on port {settings.DEBUG_PORT}")
    except Exception as e:
        print(f"⚠️  Could not start debugpy: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan event handler
    - Startup: Initialize database, worker, etc.
    - Shutdown: Cleanup resources
    """
    # Startup
    await sessionmanager.init_db()
    print("✅ Database initialized")
    worker.start()
    yield
    # Shutdown
    await worker.stop()
    await sessionmanager.close()
    print("✅ Shutdown complete")


def create_application() -> FastAPI:
    """
    Application factory pattern
    Creates and configures the FastAPI application
    """
    app = FastAPI(
        title=settings.APP_NAME,
        description="Async image generation API with job queue",
        version=settings.VERSION,
        lifespan=lifespan
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_CREDENTIALS,
        allow_methods=settings.CORS_METHODS,
        allow_headers=settings.CORS_HEADERS,
    )

    # Register routers
    app.include_router(generations_router)

    # Root endpoints
    @app.get("/", tags=["root"])
    async def root() -> dict[str, str]:  # type: ignore[misc]
        return {
            "message": settings.APP_NAME,
            "version": settings.VERSION,
            "docs": "/docs"
        }

    @app.get("/health", tags=["health"])
    async def health() -> dict[str, str]:  # type: ignore[misc]
        return {
            "status": "ok",
            "version": settings.VERSION
        }

    return app


# Create application instance
app = create_application()
