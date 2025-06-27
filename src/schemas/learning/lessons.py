from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class LessonsSchema(BaseModel):
    lesson_id: int
    title: str
    created_at: datetime
    updated_at: datetime


class LessonsNestedSchema(LessonsSchema):
    exercises: list["ExerciseSchema"]
    courses: list["CoursesSchema"]


class CreateLessonsSchema(BaseModel):
    title: str


class UpdateLessonsSchema(BaseModel):
    title: Optional[str] = None


class UpdateLessonsExerciseSchema(BaseModel):
    add_exercises_ids: list[int]
    delete_exercises_ids: list[int]


class UpdateLessonsCoursesSchema(BaseModel):
    add_courses_ids: list[int]
    delete_courses_ids: list[int]
