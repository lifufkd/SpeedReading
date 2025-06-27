from abc import ABC, abstractmethod

from src.models.lesson import Lessons
from src.dto.lessons import CreateLessonsDTO


class LessonsAbstract(ABC):

    @abstractmethod
    async def get_all(self) -> list[Lessons]:
        pass

    @abstractmethod
    async def add(self, data: CreateLessonsDTO) -> Lessons:
        pass

    @abstractmethod
    async def get_by_id(self, exercise_id: int) -> Lessons:
        pass

    @abstractmethod
    async def add(self, data: CreateLessonsDTO) -> Lessons:
        pass

    @abstractmethod
    async def delete(self, exercise_id: int) -> bool | None:
        pass
