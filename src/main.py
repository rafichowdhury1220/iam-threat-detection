"""FastAPI application factory and entry point"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from .api import router
from .core.config import settings
from .core.logger import setup_logging, get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management"""
    # Startup
    logger.info("Starting IAM Threat Detection System", version=settings.app_version)
    yield
    # Shutdown
    logger.info("Shutting down IAM Threat Detection System")


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    # Setup logging
    setup_logging()
    
    # Create app
    app = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        description="Enterprise-grade Identity and Access Management Threat Detection",
        lifespan=lifespan,
        debug=settings.debug,
    )

    # Security middleware
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["localhost", "127.0.0.1"],
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=settings.cors_credentials,
        allow_methods=settings.cors_methods,
        allow_headers=settings.cors_headers,
    )

    # Health check endpoint
    @app.get("/health")
    async def health_check() -> dict:
        """System health check"""
        return {
            "status": "healthy",
            "version": settings.app_version,
            "environment": settings.environment,
        }

    # Status endpoint
    @app.get("/status")
    async def status() -> dict:
        """System status with configuration info"""
        return {
            "app_name": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
            "features": {
                "mfa_enabled": settings.enable_mfa,
                "audit_logging": settings.enable_audit_logging,
                "threat_detection": settings.enable_threat_detection,
                "metrics_enabled": settings.enable_metrics,
            },
        }

    # Include API routes
    app.include_router(router)

    logger.info("FastAPI application initialized successfully")
    return app


# Application instance
app = create_app()
