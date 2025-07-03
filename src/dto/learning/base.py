from pydantic import BaseModel

from src.schemas.enums import TaskTypes


class UpdateTaskRelationDTOBase(BaseModel):
    task_type: TaskTypes
    add_ids: list[int]
    delete_ids: list[int]
