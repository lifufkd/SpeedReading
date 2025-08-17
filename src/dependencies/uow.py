from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session import get_session
from src.uow.sqlalchemy_uow import SQLAlchemyUoW


async def get_uow(db_session: AsyncSession = Depends(get_session)):
    return SQLAlchemyUoW(db_session)
