from sqlalchemy.ext.asyncio import AsyncSession

from src.uow.abstract import AbstractUoW
from src.repositories.users import UserRepository


class SQLAlchemyUoW(AbstractUoW):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.user_repository = UserRepository(self._session)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()
