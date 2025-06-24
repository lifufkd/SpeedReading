from src.uow.abstract import AbstractUoW
from src.core.exceptions import UserAlreadyExists
from src.services.users import UsersService
from src.core.orm_to_dto import many_sqlalchemy_to_pydantic
from src.dto.users import GetUsersDTO, CreateUsersDTO
from src.core.orm_to_dto import sqlalchemy_to_pydantic


class AdminPanelService:
    def __init__(self, uow: AbstractUoW):
        self.uow = uow
        self.users_service = UsersService(uow)

    async def get_all_users(self) -> list[GetUsersDTO]:
        async with self.uow as uow:
            users = await uow.user_repository.get_all()
            users = await many_sqlalchemy_to_pydantic(
                users,
                GetUsersDTO
            )

            return users

    async def create_user(self, user_name: str, data: CreateUsersDTO) -> GetUsersDTO:
        async with self.uow as uow:
            user = await self.users_service.get_user_by_name(name=user_name)
            if user:
                raise UserAlreadyExists()

            new_user = await uow.user_repository.add_user(data)
            new_user = await sqlalchemy_to_pydantic(
                new_user,
                GetUsersDTO
            )

            return new_user
