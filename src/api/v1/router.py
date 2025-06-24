from fastapi import APIRouter
from src.api.v1.endpoints import auth, admin_panel, profile

api_v1_router = APIRouter()

api_v1_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"]
)

api_v1_router.include_router(
    admin_panel.router,
    prefix="/admin-panel",
    tags=["Admin panel"]
)

api_v1_router.include_router(
    profile.router,
    prefix="/profile",
    tags=["Profile"]
)
