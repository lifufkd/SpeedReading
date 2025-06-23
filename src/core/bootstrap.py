from src.database.session import get_session
from src.services.users import UsersService
from src.uow.sqlalchemy_uow import SQLAlchemyUoW


async def create_super_admin():
    session_gen = get_session()
    session = await anext(session_gen)
    try:
        sqlalchemy_uow = SQLAlchemyUoW(session)
        users_service = UsersService(sqlalchemy_uow)
        await users_service.create_super_admin()
    except Exception as e:
        await session_gen.aclose()
