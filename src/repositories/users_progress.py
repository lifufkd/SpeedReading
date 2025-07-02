from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.abstract.users_progress import UsersProgressAbstract
from src.models.m2m import UsersProgress
from src.dto.student.progresses import UpdateUserProgressDTO


class UsersProgressRepository(UsersProgressAbstract):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_id(self, user_id: int, exercise_id: int) -> UsersProgress:
        query = (
            select(UsersProgress)
            .where(UsersProgress.user_id == user_id)
            .where(UsersProgress.exercise_id == exercise_id)
        )
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def update(self, progress: UsersProgress, data: UpdateUserProgressDTO) -> None:
        for key, value in data.model_dump().items():
            setattr(progress, key, value)

        await self._session.flush()
        await self._session.refresh(progress)
