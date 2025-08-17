from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models.lesson import Lessons
from src.repositories.abstract.lessons import LessonsAbstract
from src.dto.learning.lessons import CreateLessonsDTO, UpdateLessonsDTO


class LessonRepository(LessonsAbstract):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self) -> list[Lessons]:
        query = (
            select(Lessons)
            .options(selectinload(Lessons.exercises))
            .options(selectinload(Lessons.courses))
        )
        result = await self._session.execute(query)

        return list(result.scalars().all())

    async def get_by_id(self, lesson_id: int) -> Lessons:
        query = (
            select(Lessons)
            .where(Lessons.lesson_id == lesson_id)
        )

        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_id_exercises_nested(self, lesson_id: int) -> Lessons:
        query = (
            select(Lessons)
            .options(selectinload(Lessons.exercises))
            .where(Lessons.lesson_id == lesson_id)
        )

        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_id_full_nested(self, lesson_id: int) -> Lessons:
        query = (
            select(Lessons)
            .options(selectinload(Lessons.exercises))
            .options(selectinload(Lessons.courses))
            .where(Lessons.lesson_id == lesson_id)
        )

        result = await self._session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_ids(self, lessons_ids: list[int]) -> list[Lessons]:
        query = (
            select(Lessons)
            .filter(Lessons.lesson_id.in_(lessons_ids))
        )
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def add(self, data: CreateLessonsDTO) -> Lessons:
        new_lesson = Lessons(
            **data.model_dump()
        )
        self._session.add(new_lesson)
        await self._session.flush()
        await self._session.refresh(new_lesson)

        return new_lesson

    async def update(self, lesson_id: int, data: UpdateLessonsDTO) -> Lessons | None:
        lesson = await self.get_by_id(lesson_id)
        if not lesson:
            return None

        for field, value in data.model_dump(exclude_none=True).items():
            setattr(lesson, field, value)

        await self._session.flush()
        await self._session.refresh(lesson)

        return lesson

    async def delete(self, lesson_id: int) -> bool | None:
        lesson = await self.get_by_id(lesson_id)
        if not lesson:
            return None
        await self._session.delete(lesson)

        return True
