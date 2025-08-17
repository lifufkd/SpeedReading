from abc import ABC, abstractmethod
from typing import TypeVar

from src.models.users import Users
from src.dto.users.base import CreateUserDTOBase, UpdateUserDTOBase, FilterUserDTOBase


TGET_ALL = TypeVar("TGET_ALL", bound=FilterUserDTOBase)
TADD = TypeVar("TADD", bound=CreateUserDTOBase)
TUPDATE = TypeVar("TUPDATE", bound=UpdateUserDTOBase)


class UserAbstract(ABC):

    @abstractmethod
    async def get_all(self) -> list[Users]:
        pass

    @abstractmethod
    async def get_all_full_nested(self, filter: type[TGET_ALL] | None = None) -> list[Users]:
        pass

    @abstractmethod
    async def get_by_name(self, name: str) -> Users:
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> Users:
        pass

    @abstractmethod
    async def get_by_id_tasks_nested(self, user_id: int) -> Users:
        pass

    @abstractmethod
    async def get_by_id_progress_nested(self, user_id: int) -> Users:
        pass

    @abstractmethod
    async def get_by_id_full_nested(self, user_id: int) -> Users:
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
