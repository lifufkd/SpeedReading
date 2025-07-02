from fastapi import APIRouter
from src.api.v1.endpoints.student import task, progress, exercise

student_router = APIRouter()

student_router.include_router(task.router, prefix="/exercises", tags=["Student Tasks"])
student_router.include_router(progress.router, prefix="/exercises", tags=["Student Progresses"])
student_router.include_router(exercise.router, prefix="/exercises", tags=["Student exercises"])
