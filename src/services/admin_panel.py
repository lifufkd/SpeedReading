from src.uow.abstract import AbstractUoW
from src.core.jwt import get_password_hash
from src.schemas.users import GetUserSchema, UpdateUserSchema, UpdateUserDTO, CreateUserDTO
from src.core.exceptions import UserAlreadyExists, UserNotFound
from src.schemas.users import CreateUserSchema


class AdminPanelService:
    def __init__(self, uow: AbstractUoW):
        self.uow = uow

    async def get_all_users(self) -> list[GetUserSchema]:
        async with self.uow as uow:
            users = await uow.user_repository.get_all()

            return [GetUserSchema.model_validate(user) for user in users]

    async def create_user(self, data: CreateUserSchema) -> GetUserSchema:
        async with self.uow as uow:
            user = await uow.user_repository.get_by_name(name=data.login)
            if user:
                raise UserAlreadyExists()

            data = CreateUserDTO(
                password_hash=get_password_hash(data.password),
                **data.model_dump()
            )
            new_user = await uow.user_repository.add_user(data)

            return GetUserSchema.model_validate(new_user)

    async def update_user(self, data: UpdateUserSchema) -> GetUserSchema:
        async with self.uow as uow:
            data = UpdateUserDTO(
                password_hash=get_password_hash(data.password) if data.password else None,
                **data.model_dump()
            )
            user = await uow.user_repository.update_user(data=data)
            if not user:
                raise UserNotFound()

            return GetUserSchema.model_validate(user)

    async def delete_user(self, user_id: int) -> None:
        async with self.uow as uow:
            user = await uow.user_repository.delete_user(user_id=user_id)
            if not user:
                raise UserNotFound()
