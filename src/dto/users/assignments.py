from src.dto.users.base import GetUserDTOBase


class GetUserNestedTasksDTO(GetUserDTOBase):
    tasks: list["UsersTasksDTO"]


class GetUserNestedProgressDTO(GetUserDTOBase):
    progress: list["UsersProgressDTO"]


class GetUserNestedDTO(GetUserNestedTasksDTO, GetUserNestedProgressDTO):
    pass
