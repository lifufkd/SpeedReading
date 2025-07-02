from pydantic import BaseModel

from src.schemas.enums import ExerciseCompleteStatus
from src.dto.base import TimestampedDTO


class GetUserProgressDTO(TimestampedDTO):
    user_id: int
    exercise_id: int
    status: ExerciseCompleteStatus


class UpdateUserProgressDTO(BaseModel):
    status: ExerciseCompleteStatus
