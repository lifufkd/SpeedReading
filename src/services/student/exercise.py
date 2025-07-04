from src.uow.abstract import AbstractUoW
from src.core.exceptions import UserNotFound, ExerciseNotFound
from src.core.orm_to_dto import sqlalchemy_to_pydantic
from src.schemas.enums import ExerciseTypes
from src.services.student.helper import StudentHelper
from src.dto.student.exercise import (
    GetDarkenedExerciseDTO,
    GetBlocksExerciseDTO,
    GetTablesExerciseDTO,
    GetSchulteExerciseDTO,
    GetEffectiveExerciseDTO
)


class ExerciseService:
    def __init__(self, uow: AbstractUoW):
        self.uow = uow
        self.student_helper = StudentHelper()

    async def get(
            self,
            user_id: int,
            exercise_id: int
    ) -> GetDarkenedExerciseDTO | GetBlocksExerciseDTO | GetTablesExerciseDTO | GetSchulteExerciseDTO | GetEffectiveExerciseDTO:
        async with self.uow as uow:
            user = await uow.user_repository.get_by_id_tasks_nested(user_id)
            if not user:
                raise UserNotFound()

            exercise = await uow.exercise_repository.get_by_id(exercise_id)
            if not exercise:
                raise ExerciseNotFound()

            user_exercises_ids = await self.student_helper.extract_exercise_ids_from_tasks(user, uow)
            if exercise_id not in user_exercises_ids:
                raise ExerciseNotFound()

            schema_map = {
                ExerciseTypes.DARKENED: GetDarkenedExerciseDTO,
                ExerciseTypes.BLOCKS: GetBlocksExerciseDTO,
                ExerciseTypes.TABLES: GetTablesExerciseDTO,
                ExerciseTypes.SCHULTE: GetSchulteExerciseDTO,
                ExerciseTypes.EFFECTIVE: GetEffectiveExerciseDTO,
            }

            exercise = await sqlalchemy_to_pydantic(
                exercise,
                schema_map.get(exercise.type)
            )

            return exercise



