from src.uow.abstract import AbstractUoW
from src.core.exceptions import UserNotFound

from src.dto.users import UpdateUsersDTO, GetUsersDTO
from src.core.orm_to_dto import sqlalchemy_to_pydantic


class UsersService:
    def __init__(self, uow: AbstractUoW):
        self.uow = uow

    async def get_by_name(self, name: str) -> GetUsersDTO | None:
        async with self.uow as uow:
            user = await uow.user_repository.get_by_name(name)
            if not user:
                return None

            user = await sqlalchemy_to_pydantic(
                user,
                GetUsersDTO
            )
            return user

    async def update(self, user_id: int, data: UpdateUsersDTO) -> GetUsersDTO:
        async with self.uow as uow:
            user = await uow.user_repository.update(user_id, data)
            if not user:
                raise UserNotFound()

            user = await sqlalchemy_to_pydantic(
                user,
                GetUsersDTO
            )
            return user

    async def delete(self, user_id: int) -> None:
        async with self.uow as uow:
            user = await uow.user_repository.delete(user_id)
            if not user:
                raise UserNotFound()
