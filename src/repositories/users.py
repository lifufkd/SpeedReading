from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.users import Users
from src.repositories.abstract.users import UserAbstract
from src.schemas.enums import UsersRoles


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

    async def add_user(self, login: str, password_hash: str, role: UsersRoles) -> Users:
        new_user = Users(login=login, password_hash=password_hash, role=role)
        self._session.add(new_user)
        await self._session.flush()
        await self._session.refresh(new_user)

        return new_user
