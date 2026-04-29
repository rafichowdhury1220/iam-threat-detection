"""API route handlers"""

from typing import List

from fastapi import APIRouter

from . import auth, users, security, audit

# Create main router
router = APIRouter(prefix="/api/v1")

# Include route modules
router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
router.include_router(users.router, prefix="/users", tags=["Users"])
router.include_router(security.router, prefix="/security", tags=["Security"])
router.include_router(audit.router, prefix="/audit", tags=["Audit"])

__all__ = ["router"]
