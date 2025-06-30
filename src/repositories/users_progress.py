from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.abstract.users_progress import UsersProgressAbstract


class UsersProgressRepository(UsersProgressAbstract):
    def __init__(self, session: AsyncSession):
        self._session = session
