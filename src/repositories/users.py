from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models.users import Users
from src.repositories.abstract.users import UserAbstract
from src.dto.users import UpdateUsersDTO, CreateUsersDTO
from src.schemas.enums import UsersRoles


class UserRepository(UserAbstract):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self) -> list[Users]:
        query = (
            select(Users)
        )
        result = await self._session.execute(query)

        return list(result.scalars().all())

    async def get_all_students(self) -> list[Users]:
        query = (
            select(Users)
            .where(Users.role == UsersRoles.USER)
            .options(selectinload(Users.tasks))
            .options(selectinload(Users.progress))
        )
        result = await self._session.execute(query)

        return list(result.scalars().all())

    async def get_by_name(self, name: str) -> Users:
        query = (
            select(Users)
            .where(Users.login == name)
        )
        result = await self._session.execute(query)
        user = result.scalar_one_or_none()
        return user

    async def get_by_id(self, user_id: int) -> Users:
        query = (
            select(Users)
            .options(selectinload(Users.tasks))
            .options(selectinload(Users.progress))
            .where(Users.user_id == user_id)
        )
        result = await self._session.execute(query)
        user = result.scalar_one_or_none()
        return user

    async def add(self, data: CreateUsersDTO) -> Users:
        new_user = Users(
            **data.model_dump(exclude_none=True)
        )
        self._session.add(new_user)
        await self._session.flush()
        await self._session.refresh(new_user)

        return new_user

    async def update(self, user_id: int, data: UpdateUsersDTO) -> Users | None:
        user = await self.get_by_id(user_id)
        if not user:
            return None

        for field, value in data.model_dump(exclude_none=True).items():
            setattr(user, field, value)

        await self._session.flush()
        await self._session.refresh(user)

        return user

    async def delete(self, user_id: int) -> bool | None:
        user = await self.get_by_id(user_id)
        if not user:
            return None
        await self._session.delete(user)

        return True
