from abc import ABC, abstractmethod

from src.models.m2m import UsersProgress
from src.dto.student.progresses import UpdateUserProgressDTO


class UsersProgressAbstract(ABC):

    @abstractmethod
    async def get_by_id(self, user_id: int, exercise_id: int) -> UsersProgress:
        pass

    @abstractmethod
    async def update(self, progress: UsersProgress, data: UpdateUserProgressDTO) -> None:
        pass
