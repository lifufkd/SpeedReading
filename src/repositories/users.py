from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import TypeVar

from src.models.users import Users
from src.repositories.abstract.users import UserAbstract
from src.dto.users.base import UpdateUserDTOBase, CreateUserDTOBase, FilterUserDTOBase


TGET_ALL = TypeVar("TGET_ALL", bound=FilterUserDTOBase)
TADD = TypeVar("TADD", bound=CreateUserDTOBase)
TUPDATE = TypeVar("TUPDATE", bound=UpdateUserDTOBase)


class UserRepository(UserAbstract):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self, filter: type[TGET_ALL] | None = None) -> list[Users]:
        query = select(Users)
        if filter:
            query = query.filter_by(**filter.model_dump(exclude_none=True))

        result = await self._session.execute(query)

        return list(result.scalars().all())

    async def get_all_full_nested(self, filter: type[TGET_ALL] | None = None) -> list[Users]:
        query = (
            select(Users)
            .options(selectinload(Users.tasks))
            .options(selectinload(Users.progress))
        )
        if filter:
            query = query.filter_by(**filter.model_dump(exclude_none=True))

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
            .where(Users.user_id == user_id)
        )

        result = await self._session.execute(query)
        user = result.scalar_one_or_none()
        return user

    async def get_by_id_tasks_nested(self, user_id: int) -> Users:
        query = (
            select(Users)
            .options(selectinload(Users.tasks))
            .where(Users.user_id == user_id)
        )

        result = await self._session.execute(query)
        user = result.scalar_one_or_none()
        return user

    async def get_by_id_progress_nested(self, user_id: int) -> Users:
        query = (
            select(Users)
            .options(selectinload(Users.progress))
            .where(Users.user_id == user_id)
        )

        result = await self._session.execute(query)
        user = result.scalar_one_or_none()
        return user

    async def get_by_id_full_nested(self, user_id: int) -> Users:
        query = (
            select(Users)
            .options(selectinload(Users.tasks))
            .options(selectinload(Users.progress))
            .where(Users.user_id == user_id)
        )

        result = await self._session.execute(query)
        user = result.scalar_one_or_none()
        return user

    async def add(self, data: type[TADD]) -> Users:
        new_user = Users(
            **data.model_dump(exclude_none=True)
        )
        self._session.add(new_user)
        await self._session.flush()
        await self._session.refresh(new_user)

        return new_user

    async def update(self, user_id: int, data: type[TUPDATE]) -> Users | None:
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
