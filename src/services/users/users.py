from src.uow.abstract import AbstractUoW
from src.core.exceptions import UserNotFound, UserAlreadyExists

from src.dto.users.base import UpdateUserDTOBase, GetUserDTOBase
from src.core.orm_to_dto import sqlalchemy_to_pydantic


class UsersService:
    def __init__(self, uow: AbstractUoW):
        self.uow = uow

    async def get_by_name(self, name: str) -> GetUserDTOBase | None:
        async with self.uow as uow:
            user = await uow.user_repository.get_by_name(name)
            if not user:
                return None

            user = await sqlalchemy_to_pydantic(
                user,
                GetUserDTOBase
            )
            return user

    async def update(self, user_id: int, data: UpdateUserDTOBase) -> GetUserDTOBase:
        async with self.uow as uow:
            if data.login:
                user = await uow.user_repository.get_by_name(data.login)
                if user:
                    raise UserAlreadyExists(user_name=user.login)

            user = await uow.user_repository.update(user_id, data)
            if not user:
                raise UserNotFound()

            user = await sqlalchemy_to_pydantic(
                user,
                GetUserDTOBase
            )
            return user

    async def delete(self, user_id: int) -> None:
        async with self.uow as uow:
            user = await uow.user_repository.delete(user_id)
            if not user:
                raise UserNotFound()
