from fastapi import APIRouter
from src.api.v1.endpoints import auth, profile
from src.api.v1.endpoints.admin import admin_panel, exercise, lesson, course

api_v1_router = APIRouter()

api_v1_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"]
)

api_v1_router.include_router(
    admin_panel.router,
    prefix="/admin/admin-panel",
    tags=["Admin panel"]
)

api_v1_router.include_router(
    profile.router,
    prefix="/profile",
    tags=["Profile"]
)

api_v1_router.include_router(
    exercise.router,
    prefix="/admin/exercise",
    tags=["Exercise"]
)

api_v1_router.include_router(
    lesson.router,
    prefix="/admin/lesson",
    tags=["Lesson"]
)

api_v1_router.include_router(
    course.router,
    prefix="/admin/course",
    tags=["Course"]
)
