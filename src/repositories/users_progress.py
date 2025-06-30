from sqlalchemy.ext.asyncio import AsyncSession

from src.models.m2m import UsersProgress
from src.repositories.abstract.users_progress import UsersProgressAbstract
from src.dto.assignment import CreateUsersProgressDTO


class UsersProgressRepository(UsersProgressAbstract):
    def __init__(self, session: AsyncSession):
        self._session = session
