from abc import ABC, abstractmethod

from src.models.users import Users


class UserAbstract(ABC):

    @abstractmethod
    async def get_by_name(self, name: str) -> Users:
        pass
