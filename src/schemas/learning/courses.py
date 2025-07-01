from pydantic import BaseModel
from typing import Optional

from src.schemas.learning.base import UniqueFieldValidator
from src.schemas.base import TimestampedSchema


class CoursesSchema(TimestampedSchema):
    course_id: int
    title: str


class CourseFullNestedSchema(CoursesSchema):
    lessons: list["LessonNestedExercisesSchema"]
    exercises: list["ExerciseSchema"]


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
