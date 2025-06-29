from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from src.schemas.learning.base import UniqueFieldValidator


class CoursesSchema(BaseModel):
    course_id: int
    title: str
    created_at: datetime
    updated_at: datetime


class CoursesNestedSchema(CoursesSchema):
    lessons: list["LessonsSchema"]
    exercises: list["ExerciseSchema"]


class CreateCoursesSchema(BaseModel):
    title: str


class UpdateCoursesSchema(BaseModel):
    title: Optional[str] = None


class UpdateCoursesExerciseSchema(UniqueFieldValidator):
    add_exercises_ids: Optional[list[int]] = []
    delete_exercises_ids: Optional[list[int]] = []


class UpdateCoursesLessonsSchema(UniqueFieldValidator):
    add_lessons_ids: Optional[list[int]] = []
    delete_lessons_ids: Optional[list[int]] = []
