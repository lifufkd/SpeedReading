from fastapi import APIRouter
from src.api.v1.endpoints.admin import admin_panel, exercise, lesson, course, assignment

admin_router = APIRouter()

admin_router.include_router(admin_panel.router, tags=["Admin panel"])
admin_router.include_router(exercise.router, prefix="/exercises", tags=["Exercises"])
admin_router.include_router(lesson.router, prefix="/lessons", tags=["Lessons"])
admin_router.include_router(course.router, prefix="/courses", tags=["Courses"])
admin_router.include_router(assignment.router, prefix="/users", tags=["Assignments"])
