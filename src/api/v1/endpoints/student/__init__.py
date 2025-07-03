from fastapi import APIRouter, Depends

from src.api.v1.endpoints.student import task, progress, exercise
from src.dependencies.security import validate_student

student_router = APIRouter(
    dependencies=[Depends(validate_student)]
)

student_router.include_router(task.router, prefix="/exercises", tags=["Student Tasks"])
student_router.include_router(progress.router, prefix="/exercises", tags=["Student Progresses"])
student_router.include_router(exercise.router, prefix="/exercises", tags=["Student exercises"])
