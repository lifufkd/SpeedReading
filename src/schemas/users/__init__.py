from src.schemas.learning.assignment import AssignmentSchema, UsersProgressSchema # noqa
from src.schemas.users.assignments import UserNestedTasksSchema, UserNestedProgressSchema, UserNestedSchema


UserNestedTasksSchema.model_rebuild()
UserNestedProgressSchema.model_rebuild()
UserNestedSchema.model_rebuild()
