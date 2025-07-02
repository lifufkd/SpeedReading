from src.uow.abstract import AbstractUoW
from src.core.exceptions import UserNotFound, ExerciseNotFound
from src.validators.users import validate_user_is_student
from src.dto.users import GetUserNestedProgressDTO
from src.dto.student.progresses import UpdateUserProgressDTO, GetUserProgressDTO
from src.core.orm_to_dto import sqlalchemy_to_pydantic


class ProgressService:
    def __init__(self, uow: AbstractUoW):
        self.uow = uow

    async def get(self, user_id: int) -> GetUserNestedProgressDTO:
        async with self.uow as uow:
            user = await uow.user_repository.get_by_id(user_id)
            if not user:
                raise UserNotFound()
            await validate_user_is_student(user)   # TODO: User must be as DTO object

            user = await sqlalchemy_to_pydantic(
                user,
                GetUserNestedProgressDTO
            )

            return user

    async def update(self, user_id: int, exercise_id: int, data: UpdateUserProgressDTO) -> GetUserProgressDTO:
        async with self.uow as uow:
            user = await uow.user_repository.get_by_id(user_id)
            if not user:
                raise UserNotFound()
            await validate_user_is_student(user)  # TODO: User must be as DTO object

            user_progress = await uow.users_progress_repository.get_by_id(user_id, exercise_id)
            if not user_progress:
                raise ExerciseNotFound()

            await uow.users_progress_repository.update(user_progress, data)

            user_progress = await sqlalchemy_to_pydantic(
                user_progress,
                GetUserProgressDTO
            )

            return user_progress
