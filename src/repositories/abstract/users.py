from abc import ABC, abstractmethod

from src.models.users import Users
from src.dto.users.base import CreateUserDTOBase, UpdateUserDTOBase


class UserAbstract(ABC):

    @abstractmethod
    async def get_all(self) -> list[Users]:
        pass

    @abstractmethod
    async def get_by_name(self, name: str) -> Users:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Users:
        pass

    @abstractmethod
    async def add(self, data: CreateUserDTOBase) -> Users:
        pass

    @abstractmethod
    async def update(self, user_id: int, data: UpdateUserDTOBase) -> Users | None:
        pass

    @abstractmethod
    async def delete(self, user_id: int) -> bool | None:
        pass
