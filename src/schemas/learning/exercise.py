from pydantic import BaseModel
from typing import Optional

from src.schemas.learning.base import UniqueFieldValidator
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


class UpdateExerciseLessonsSchema(UniqueFieldValidator):
    add_lessons_ids: Optional[list[int]] = []
    delete_lessons_ids: Optional[list[int]] = []


class UpdateExerciseCoursesSchema(UniqueFieldValidator):
    add_courses_ids: Optional[list[int]] = []
    delete_courses_ids: Optional[list[int]] = []
