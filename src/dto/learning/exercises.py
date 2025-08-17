from pydantic import BaseModel
from typing import Optional

from src.schemas.enums import ExerciseTypes
from src.dto.base import TimestampedDTO


class GetExercisesDTO(TimestampedDTO):
    exercise_id: int
    title: str
    type: ExerciseTypes


class GetNestedExercisesDTO(GetExercisesDTO):
    lessons: list["GetLessonsDTO"]
    courses: list["GetCoursesDTO"]


class CreateExerciseDTO(BaseModel):
    title: str
    type: ExerciseTypes


class UpdateExerciseDTO(BaseModel):
    title: Optional[str] = None
    type: Optional[ExerciseTypes] = None
