from abc import ABC, abstractmethod

from src.models.lesson import Lessons
from src.dto.learning.lessons import CreateLessonsDTO, UpdateLessonsDTO


class LessonsAbstract(ABC):

    @abstractmethod
    async def get_all(self) -> list[Lessons]:
        pass

    @abstractmethod
    async def get_by_id(self, lesson_id: int) -> Lessons:
        pass

    @abstractmethod
    async def get_by_id_exercises_nested(self, lesson_id: int) -> Lessons:
        pass

    @abstractmethod
    async def get_by_id_full_nested(self, lesson_id: int) -> Lessons:
        pass

    @abstractmethod
    async def get_by_ids(self, lessons_ids: list[int]) -> list[Lessons]:
        pass

    @abstractmethod
    async def add(self, data: CreateLessonsDTO) -> Lessons:
        pass

    @abstractmethod
    async def update(self, lesson_id: int, data: UpdateLessonsDTO) -> Lessons | None:
        pass

    @abstractmethod
    async def delete(self, lesson_id: int) -> bool | None:
        pass
