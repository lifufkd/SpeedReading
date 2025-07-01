from src.database.session import get_session
from src.services.users.super_admin_init import SuperAdminInitService
from src.uow.sqlalchemy_uow import SQLAlchemyUoW
from src.core.config import generic_settings
from src.dto.users.base import CreateUserDTOBase
from src.core.jwt import get_password_hash
from src.schemas.enums import UsersRoles


async def create_super_admin():
    session_gen = get_session()
    session = await anext(session_gen)
    try:
        super_admin_login = generic_settings.SUPER_ADMIN_LOGIN
        super_admin_password = generic_settings.SUPER_ADMIN_PASSWORD

        sqlalchemy_uow = SQLAlchemyUoW(session)
        super_admin_init_service = SuperAdminInitService(sqlalchemy_uow)
        data = CreateUserDTOBase(
            login=super_admin_login,
            password_hash=get_password_hash(super_admin_password),
            role=UsersRoles.ADMIN
        )
        await super_admin_init_service.create_super_admin(
            user_name=super_admin_login,
            data=data
        )
    finally:
        await session_gen.aclose()
