from src.uow.abstract import AbstractUoW
from src.core.exceptions import UserNotFound, ExerciseNotFound
from src.core.orm_to_dto import sqlalchemy_to_pydantic
from src.dto.student.exercise import GetDarkenedExerciseDTO


class ExerciseService:
    def __init__(self, uow: AbstractUoW):
        self.uow = uow

    async def get(self, user_id: int, exercise_id: int) -> GetDarkenedExerciseDTO:
        async with self.uow as uow:
            user = await uow.user_repository.get_by_id(user_id)
            if not user:
                raise UserNotFound()

            exercise = await uow.exercise_repository.get_by_id(exercise_id)
            if not exercise:
                raise ExerciseNotFound()

            exercise = await sqlalchemy_to_pydantic(
                exercise,
                GetDarkenedExerciseDTO
            )

            return exercise



