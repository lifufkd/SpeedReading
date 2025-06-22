from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.users import Users
from src.repositories.abstract.users import UserAbstract


class UserRepository(UserAbstract):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_name(self, name: str) -> Users:
        query = (
            select(Users)
            .where(Users.login == name)
        )
        result = await self._session.execute(query)
        user = result.scalar_one_or_none()
        return user
