from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from src.schemas.learning.base import UniqueFieldValidator
from src.schemas.enums import ExerciseTypes


class ExerciseSchema(BaseModel):
    exercise_id: int
    title: str
    type: ExerciseTypes
    created_at: datetime
    updated_at: datetime


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
