from abc import ABC, abstractmethod

from src.schemas.enums import TaskTypes
from src.models.users_tasks import UsersTasks


class UsersTasksAbstract(ABC):

    @abstractmethod
    async def get_by_task_type(self, user_id: int, task_type: TaskTypes) -> list[UsersTasks]:
        pass

