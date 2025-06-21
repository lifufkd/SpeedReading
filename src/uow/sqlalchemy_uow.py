from sqlalchemy.ext.asyncio import AsyncSession

from src.uow.abstract import AbstractUoW


class SQLAlchemyUoW(AbstractUoW):
    def __init__(self, session: AsyncSession):
        pass
