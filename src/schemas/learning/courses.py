from pydantic import BaseModel
from typing import Optional
from datetime import datetime


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


class UpdateCoursesExerciseSchema(BaseModel):
    add_exercises_ids: list[int]
    delete_exercises_ids: list[int]


class UpdateCoursesLessonsSchema(BaseModel):
    add_lessons_ids: list[int]
    delete_lessons_ids: list[int]
