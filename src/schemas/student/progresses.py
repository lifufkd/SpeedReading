from pydantic import BaseModel

from src.schemas.enums import ExerciseCompleteStatus
from src.schemas.base import TimestampedSchema


class UserProgressSchema(TimestampedSchema):
    user_id: int
    exercise_id: int
    status: ExerciseCompleteStatus


class UpdateUserProgressSchema(BaseModel):
    status: ExerciseCompleteStatus
