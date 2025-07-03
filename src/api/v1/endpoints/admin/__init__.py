from fastapi import APIRouter, Depends

from src.api.v1.endpoints.admin import admin_panel, exercise, lesson, course, assignment
from src.dependencies.security import validate_admin

admin_router = APIRouter(
    dependencies=[Depends(validate_admin)]
)

admin_router.include_router(admin_panel.router, tags=["Admin panel"])
admin_router.include_router(exercise.router, prefix="/exercises", tags=["Exercises"])
admin_router.include_router(lesson.router, prefix="/lessons", tags=["Lessons"])
admin_router.include_router(course.router, prefix="/courses", tags=["Courses"])
admin_router.include_router(assignment.router, prefix="/users", tags=["Assignments"])
