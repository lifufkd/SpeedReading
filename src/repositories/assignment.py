from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.models.users_tasks import UsersTasks
from src.repositories.abstract.assignment import AssignmentAbstract
from src.schemas.enums import TaskTypes


class AssignmentRepository(AssignmentAbstract):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_task_type(self, user_id: int, task_type: TaskTypes) -> list[UsersTasks]:
        query = (
            select(UsersTasks)
            .where(UsersTasks.user_id == user_id)
            .where(UsersTasks.task_type == task_type)
        )
        result = await self._session.execute(query)

        return list(result.scalars().all())
