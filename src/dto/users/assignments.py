from src.dto.users.base import GetUserDTOBase, FilterUserDTOBase
from src.schemas.enums import UsersRoles


class GetUserNestedTasksDTO(GetUserDTOBase):
    tasks: list["UsersTasksDTO"]


class GetUserNestedProgressDTO(GetUserDTOBase):
    progress: list["UsersProgressDTO"]


class GetUserNestedDTO(GetUserNestedTasksDTO, GetUserNestedProgressDTO):
    pass


class FilterUserDTO(FilterUserDTOBase):
    role: UsersRoles
