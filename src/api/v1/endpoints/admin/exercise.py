from fastapi import APIRouter, status, Depends, Body, Path

from src.services.learning.exercise import ExerciseService
from src.dependencies.security import validate_token, validate_admin
from src.dependencies.services import get_exercise_service
from src.dto.learning.exercises import (
    CreateExerciseDTO,
    UpdateExerciseDTO
)
from src.core.dto_to_schema import many_dto_to_schema, dto_to_schema
from src.schemas.learning.exercise import (
    ExerciseNestedSchema,
    CreateExerciseSchema,
    ExerciseSchema,
    UpdateExerciseSchema

)

router = APIRouter(
    dependencies=[Depends(validate_token), Depends(validate_admin)],
)


@router.get("", status_code=status.HTTP_200_OK, response_model=list[ExerciseNestedSchema])
async def get_exercises(
        exercise_service: ExerciseService = Depends(get_exercise_service)
):

    exercises = await exercise_service.get_all()
    exercises = await many_dto_to_schema(
        exercises,
        ExerciseNestedSchema
    )

    return exercises


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ExerciseSchema)
async def create_exercise(
        request: CreateExerciseSchema = Body(),
        exercise_service: ExerciseService = Depends(get_exercise_service)
):
    data = CreateExerciseDTO(
        **request.model_dump()
    )
    new_exercise = await exercise_service.create(data)
    new_exercise = await dto_to_schema(
        new_exercise,
        ExerciseSchema
    )

    return new_exercise


@router.patch("/{exercise_id}", status_code=status.HTTP_200_OK, response_model=ExerciseSchema)
async def update_exercise(
        exercise_id: int = Path(),
        request: UpdateExerciseSchema = Body(),
        exercise_service: ExerciseService = Depends(get_exercise_service)
):
    data = UpdateExerciseDTO(
        **request.model_dump()
    )
    exercise = await exercise_service.update(exercise_id, data)
    exercise = await dto_to_schema(
        exercise,
        ExerciseSchema
    )

    return exercise


@router.delete("/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_exercise(
        exercise_id: int = Path(),
        exercise_service: ExerciseService = Depends(get_exercise_service)
):
    await exercise_service.delete(exercise_id)
