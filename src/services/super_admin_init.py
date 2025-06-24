from src.uow.abstract import AbstractUoW
from src.services.users import UsersService
from src.dto.users import GetUsersDTO, CreateUsersDTO
from src.core.orm_to_dto import sqlalchemy_to_pydantic


class SuperAdminInitService:
    def __init__(self, uow: AbstractUoW):
        self.uow = uow
        self.users_service = UsersService(uow)

    async def create_super_admin(self, user_name: str, data: CreateUsersDTO) -> GetUsersDTO | None:
        async with self.uow as uow:
            user = await self.users_service.get_user_by_name(name=user_name)
            if user:
                return None

            super_admin = await uow.user_repository.add_user(data)
            super_admin = await sqlalchemy_to_pydantic(
                super_admin,
                GetUsersDTO
            )

            return super_admin
