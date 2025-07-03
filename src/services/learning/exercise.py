from src.uow.abstract import AbstractUoW
from src.core.exceptions import ExerciseNotFound
from src.core.orm_to_dto import many_sqlalchemy_to_pydantic
from src.core.orm_to_dto import sqlalchemy_to_pydantic
from src.dto.learning.assignment import FilterUsersTasksDTO
from src.dto.learning.exercises import (
    GetExercisesDTO,
    GetNestedExercisesDTO,
    CreateExerciseDTO,
    UpdateExerciseDTO
)
from src.schemas.enums import TaskTypes


class ExerciseService:
    def __init__(self, uow: AbstractUoW):
        self.uow = uow

    async def get_by_id(self, exercise_id: int) -> GetExercisesDTO:
        async with self.uow as uow:
            exercise = await uow.exercise_repository.get_by_id(exercise_id)
            if not exercise:
                raise ExerciseNotFound()

            exercise = await sqlalchemy_to_pydantic(
                exercise,
                GetExercisesDTO
            )

            return exercise

    async def get_all(self) -> list[GetNestedExercisesDTO]:
        async with self.uow as uow:
            exercises = await uow.exercise_repository.get_all()
            exercises = await many_sqlalchemy_to_pydantic(
                exercises,
                GetNestedExercisesDTO
            )

            return exercises

    async def create(self, data: CreateExerciseDTO) -> GetExercisesDTO:
        async with self.uow as uow:
            new_exercise = await uow.exercise_repository.add(data)
            new_exercise = await sqlalchemy_to_pydantic(
                new_exercise,
                GetExercisesDTO
            )

            return new_exercise

    async def update(self, exercise_id: int, data: UpdateExerciseDTO) -> GetExercisesDTO:
        async with self.uow as uow:
            exercise = await uow.exercise_repository.update(exercise_id, data)
            if not exercise:
                raise ExerciseNotFound()

            exercise = await sqlalchemy_to_pydantic(
                exercise,
                GetExercisesDTO
            )
            return exercise

    async def delete(self, exercise_id: int) -> None:
        async with self.uow as uow:
            exercise = await uow.exercise_repository.delete(exercise_id)
            if not exercise:
                raise ExerciseNotFound()

            data = FilterUsersTasksDTO(
                task_id=exercise_id,
                task_type=TaskTypes.EXERCISE
            )
            await uow.users_tasks_repository.delete(data)
