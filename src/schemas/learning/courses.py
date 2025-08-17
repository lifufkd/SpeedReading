from pydantic import BaseModel
from typing import Optional

from src.schemas.base import TimestampedSchema
from src.schemas.learning.base import UpdateTaskRelationSchemaBase


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


class UpdateCourseRelationSchema(UpdateTaskRelationSchemaBase):
    pass
