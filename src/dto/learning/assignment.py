from pydantic import BaseModel
from typing import Optional

from src.schemas.enums import TaskTypes
from src.schemas.enums import ExerciseCompleteStatus
from src.dto.base import TimestampedDTO
from src.dto.learning.base import UpdateTaskRelationDTOBase


class UsersTasksDTO(TimestampedDTO):
    users_tasks_id: int
    user_id: int
    task_id: int
    task_type: TaskTypes


class UsersProgressDTO(TimestampedDTO):
    user_id: int
    exercise_id: int
    status: ExerciseCompleteStatus


class FilterUsersTasksDTO(BaseModel):
    users_tasks_id: Optional[int] = None
    user_id: Optional[int] = None
    task_id: Optional[int] = None
    task_type: Optional[TaskTypes] = None


class UpdateAssignedTasksDTO(UpdateTaskRelationDTOBase):
    pass
