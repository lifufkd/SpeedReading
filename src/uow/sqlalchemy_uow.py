from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.users_progress import UsersProgressRepository
from src.repositories.users_tasks import UsersTasksRepository
from src.repositories.courses import CourseRepository
from src.uow.abstract import AbstractUoW
from src.repositories.users import UserRepository
from src.repositories.exercises import ExerciseRepository
from src.repositories.lessons import LessonRepository


class SQLAlchemyUoW(AbstractUoW):
    def __init__(self, session: AsyncSession):
        self._session = session
        self.user_repository = UserRepository(session)
        self.exercise_repository = ExerciseRepository(session)
        self.lesson_repository = LessonRepository(session)
        self.course_repository = CourseRepository(session)
        self.users_tasks_repository = UsersTasksRepository(session)
        self.users_progress_repository = UsersProgressRepository(session)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        else:
            await self.commit()

    async def commit(self):
        await self._session.commit()

    async def flush(self):
        await self._session.flush()

    async def rollback(self):
        await self._session.rollback()
