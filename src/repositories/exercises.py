from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.models.exercise import Exercises
from src.repositories.abstract.exercises import ExerciseAbstract
from src.dto.exercises import CreateExerciseDTO, UpdateExerciseDTO


class ExerciseRepository(ExerciseAbstract):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self) -> list[Exercises]:
        query = (
            select(Exercises)
            .options(selectinload(Exercises.lessons))
            .options(selectinload(Exercises.courses))
        )
        result = await self._session.execute(query)

        return list(result.scalars().all())

    async def get_by_id(self, exercise_id: int) -> Exercises:
        query = (
            select(Exercises)
            .where(Exercises.exercise_id == exercise_id)
        )
        result = await self._session.execute(query)
        exercise = result.scalar_one_or_none()
        return exercise

    async def add(self, data: CreateExerciseDTO) -> Exercises:
        new_exercise = Exercises(
            **data.model_dump()
        )
        self._session.add(new_exercise)
        await self._session.flush()
        await self._session.refresh(new_exercise)

        return new_exercise

    async def update(self, exercise_id: int, data: UpdateExerciseDTO) -> Exercises | None:
        exercise = await self.get_by_id(exercise_id)
        if not exercise:
            return None

        for field, value in data.model_dump(exclude_none=True).items():
            setattr(exercise, field, value)

        await self._session.flush()
        await self._session.refresh(exercise)

        return exercise

    async def delete(self, exercise_id: int) -> bool | None:
        exercise = await self.get_by_id(exercise_id)
        if not exercise:
            return None
        await self._session.delete(exercise)

        return True
