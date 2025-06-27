from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models.course import Courses
from src.repositories.abstract.courses import CoursesAbstract
from src.dto.courses import CreateCoursesDTO, UpdateCoursesDTO


class CourseRepository(CoursesAbstract):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self) -> list[Courses]:
        query = (
            select(Courses)
            .options(selectinload(Courses.exercises))
            .options(selectinload(Courses.lessons))
        )
        result = await self._session.execute(query)

        return list(result.scalars().all())

    async def get_by_id(self, course_id: int) -> Courses:
        query = (
            select(Courses)
            .where(Courses.course_id == course_id)
        )
        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_ids(self, courses_ids: list[int]) -> list[Courses]:
        query = (
            select(Courses)
            .filter(Courses.course_id.in_(courses_ids))
        )
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def add(self, data: CreateCoursesDTO) -> Courses:
        new_course = Courses(
            **data.model_dump()
        )
        self._session.add(new_course)
        await self._session.flush()
        await self._session.refresh(new_course)

        return new_course

    async def update(self, course_id: int, data: UpdateCoursesDTO) -> Courses | None:
        course = await self.get_by_id(course_id)
        if not course:
            return None

        for field, value in data.model_dump(exclude_none=True).items():
            setattr(course, field, value)

        await self._session.flush()
        await self._session.refresh(course)

        return course

    async def delete(self, course_id: int) -> bool | None:
        course = await self.get_by_id(course_id)
        if not course:
            return None
        await self._session.delete(course)

        return True
