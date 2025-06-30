from src.schemas.learning.assignment import AssignmentSchema, UsersProgressSchema # noqa
from src.schemas.users.base import UserNestedTasksSchema, UserNestedProgressSchema, UserNestedSchema


UserNestedTasksSchema.model_rebuild()
UserNestedProgressSchema.model_rebuild()
UserNestedSchema.model_rebuild()
