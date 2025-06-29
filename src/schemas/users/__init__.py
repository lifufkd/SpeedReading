from src.schemas.learning.assignment import AssignmentSchema # noqa
from src.schemas.users.base import UserNestedSchema


UserNestedSchema.model_rebuild()
