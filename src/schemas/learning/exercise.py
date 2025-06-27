from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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


class UpdateExerciseLessonsSchema(BaseModel):
    add_lessons_ids: list[int]
    delete_lessons_ids: list[int]


class UpdateExerciseCoursesSchema(BaseModel):
    add_courses_ids: list[int]
    delete_courses_ids: list[int]
