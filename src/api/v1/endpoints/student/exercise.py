from fastapi import APIRouter, status, Depends, Path

from src.services.student.exercise import ExerciseService as StudentExerciseService
from src.dependencies.security import validate_token
from src.dependencies.services import get_student_exercise_service
from src.dto.users.auth import GetUserDTO
from src.schemas.student.exercises import (
    DarkenedExerciseSchema,
    BlocksExerciseSchema,
    TablesExerciseSchema,
    SchulteExerciseSchema,
    EffectiveExerciseSchema
)
from src.core.dto_to_schema import dto_to_schema
from src.schemas.enums import ExerciseTypes

router = APIRouter()


@router.get(
    "/{exercise_id}",
    status_code=status.HTTP_200_OK,
    response_model=DarkenedExerciseSchema | BlocksExerciseSchema | TablesExerciseSchema | SchulteExerciseSchema | EffectiveExerciseSchema
)
async def get_full_exercise(
        exercise_id: int = Path(),
        current_user: GetUserDTO = Depends(validate_token),
        student_exercise_service: StudentExerciseService = Depends(get_student_exercise_service),
):
    task = await student_exercise_service.get(current_user.user_id, exercise_id)

    schema_map = {
        ExerciseTypes.DARKENED: DarkenedExerciseSchema,
        ExerciseTypes.BLOCKS: BlocksExerciseSchema,
        ExerciseTypes.TABLES: TablesExerciseSchema,
        ExerciseTypes.SCHULTE: SchulteExerciseSchema,
        ExerciseTypes.EFFECTIVE: EffectiveExerciseSchema,
    }

    schema_class = schema_map.get(task.type)
    task = await dto_to_schema(
        task,
        schema_class
    )
    return task
