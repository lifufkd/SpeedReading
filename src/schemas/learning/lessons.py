from pydantic import BaseModel
from typing import Optional

from src.schemas.learning.base import UniqueFieldValidator
from src.schemas.base import TimestampedSchema


class LessonsSchema(TimestampedSchema):
    lesson_id: int
    title: str


class LessonNestedExercisesSchema(LessonsSchema):
    exercises: list["ExerciseSchema"]


class LessonsNestedSchema(LessonsSchema):
    exercises: list["ExerciseSchema"]
    courses: list["CoursesSchema"]


class CreateLessonsSchema(BaseModel):
    title: str


class UpdateLessonsSchema(BaseModel):
    title: Optional[str] = None


class UpdateLessonsExerciseSchema(UniqueFieldValidator):
    add_exercises_ids: Optional[list[int]] = []
    delete_exercises_ids: Optional[list[int]] = []


class UpdateLessonsCoursesSchema(UniqueFieldValidator):
    add_courses_ids: Optional[list[int]] = []
    delete_courses_ids: Optional[list[int]] = []
