from src.schemas.enums import TaskTypes, ExerciseCompleteStatus
from src.schemas.learning.base import UpdateTaskRelationSchemaBase
from src.schemas.base import TimestampedSchema


class AssignmentSchema(TimestampedSchema):
    users_tasks_id: int
    user_id: int
    task_id: int
    task_type: TaskTypes


class UsersProgressSchema(TimestampedSchema):
    user_id: int
    exercise_id: int
    status: ExerciseCompleteStatus


class UpdateAssignedTasksSchema(UpdateTaskRelationSchemaBase):
    pass
