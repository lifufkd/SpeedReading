from src.uow.abstract import AbstractUoW
from src.core.config import generic_settings
from src.core.jwt import get_password_hash
from src.schemas.enums import UsersRoles
from src.schemas.users import UserSchema


class SuperAdminInitService:
    def __init__(self, uow: AbstractUoW):
        self.uow = uow

    async def create_super_admin(self):
        super_admin_login = generic_settings.SUPER_ADMIN_LOGIN
        super_admin_password = generic_settings.SUPER_ADMIN_PASSWORD
        async with self.uow as uow:
            user = await uow.user_repository.get_by_name(name=super_admin_login)
            if user:
                return None

            super_admin = await uow.user_repository.add_user(
                login=super_admin_login,
                password_hash=get_password_hash(super_admin_password),
                role=UsersRoles.ADMIN
            )

            return UserSchema.model_validate(super_admin)
