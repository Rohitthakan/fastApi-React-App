from fastapi import APIRouter
from .auth import router as auth_router
from .dashboard import router as dashboard_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(dashboard_router, prefix="/dashboard", tags=["Dashboard"])
