from fastapi import APIRouter, status, Depends, Path

from src.services.student.exercise import ExerciseService as StudentExerciseService
from src.dependencies.security import validate_token
from src.dependencies.services import get_student_exercise_service
from src.dto.users.auth import GetUserDTO
from src.schemas.student.exercises import DarkenedExerciseSchema
from src.core.dto_to_schema import dto_to_schema

router = APIRouter()


@router.get("/{exercise_id}", status_code=status.HTTP_200_OK, response_model=DarkenedExerciseSchema)
async def get_full_exercise(
        exercise_id: int = Path(),
        current_user: GetUserDTO = Depends(validate_token),
        student_exercise_service: StudentExerciseService = Depends(get_student_exercise_service),
):
    tasks = await student_exercise_service.get(current_user.user_id, exercise_id)

    tasks = await dto_to_schema(
        tasks,
        DarkenedExerciseSchema
    )
    return tasks
