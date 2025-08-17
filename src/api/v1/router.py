from fastapi import APIRouter
from src.api.v1.endpoints import auth, profile
from src.api.v1.endpoints.admin import admin_router
from src.api.v1.endpoints.student import student_router

api_v1_router = APIRouter()


api_v1_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_v1_router.include_router(profile.router, prefix="/profile", tags=["Profile"])
api_v1_router.include_router(admin_router, prefix="/admin")
api_v1_router.include_router(student_router, prefix="/student")
