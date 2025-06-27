from abc import ABC, abstractmethod

from src.models.users import Users
from src.dto.users import CreateUsersDTO, UpdateUsersDTO


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
    async def add_user(self, data: CreateUsersDTO) -> Users:
        pass

    @abstractmethod
    async def update_user(self, user_id: int, data: UpdateUsersDTO) -> Users | None:
        pass

    @abstractmethod
    async def delete_user(self, user_id: int) -> bool | None:
        pass
