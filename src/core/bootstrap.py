from src.database.session import get_session
from src.services.super_admin_init import SuperAdminInitService
from src.uow.sqlalchemy_uow import SQLAlchemyUoW


async def create_super_admin():
    session_gen = get_session()
    session = await anext(session_gen)
    try:
        sqlalchemy_uow = SQLAlchemyUoW(session)
        super_admin_init_service = SuperAdminInitService(sqlalchemy_uow)
        await super_admin_init_service.create_super_admin()
    except Exception as e:
        await session_gen.aclose()
