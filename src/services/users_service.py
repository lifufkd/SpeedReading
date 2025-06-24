from src.uow.abstract import AbstractUoW
from src.core.exceptions import UserNotFound

from src.schemas.users import UpdateUserSchema, GetUserSchema, UpdateUserDTO
from src.schemas.profile import UpdateProfileSchema
from src.core.jwt import get_password_hash


class UsersService:
    def __init__(self, uow: AbstractUoW):
        self.uow = uow

    async def update_user(self, data: UpdateUserSchema | UpdateProfileSchema) -> GetUserSchema:
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
