from src.dto.learning.assignment import UsersTasksDTO, UsersProgressDTO # noqa
from src.dto.users.assignments import GetUserNestedTasksDTO, GetUserNestedProgressDTO, GetUserNestedDTO


GetUserNestedTasksDTO.model_rebuild()
GetUserNestedProgressDTO.model_rebuild()
GetUserNestedDTO.model_rebuild()
