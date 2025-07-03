from pydantic import BaseModel
from typing import Optional

from src.schemas.enums import ExerciseTypes
from src.schemas.base import TimestampedSchema


class ExerciseSchema(TimestampedSchema):
    exercise_id: int
    title: str
    type: ExerciseTypes


class ExerciseNestedSchema(ExerciseSchema):
    lessons: list["LessonsSchema"]
    courses: list["CoursesSchema"]


class CreateExerciseSchema(BaseModel):
    title: str
    type: ExerciseTypes


class UpdateExerciseSchema(BaseModel):
    title: Optional[str] = None
    type: Optional[ExerciseTypes] = None
