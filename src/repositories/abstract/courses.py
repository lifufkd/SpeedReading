from abc import ABC, abstractmethod

from src.models.course import Courses
from src.dto.learning.courses import CreateCoursesDTO, UpdateCoursesDTO


class CoursesAbstract(ABC):

    @abstractmethod
    async def get_all(self) -> list[Courses]:
        pass

    @abstractmethod
    async def get_by_id(self, course_id: int) -> Courses:
        pass

    @abstractmethod
    async def get_by_id_exercises_lessons_nested(self, course_id: int) -> Courses:
        pass

    @abstractmethod
    async def get_by_id_full_nested(self, course_id: int) -> Courses:
        pass

    @abstractmethod
    async def get_by_ids(self, courses_ids: list[int]) -> list[Courses]:
        pass

    @abstractmethod
    async def add(self, data: CreateCoursesDTO) -> Courses:
        pass

    @abstractmethod
    async def update(self, course_id: int, data: UpdateCoursesDTO) -> Courses | None:
        pass

    @abstractmethod
    async def delete(self, course_id: int) -> bool | None:
        pass
