from pydantic import BaseModel
from typing import Optional

from src.schemas.base import TimestampedSchema
from src.schemas.learning.base import UpdateTaskRelationSchemaBase


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


class UpdateLessonRelationSchema(UpdateTaskRelationSchemaBase):
    pass
