from pydantic import BaseModel
from typing import Optional

from src.dto.base import TimestampedDTO
from src.dto.learning.base import UpdateTaskRelationDTOBase


class GetCoursesDTO(TimestampedDTO):
    course_id: int
    title: str


class GetCourseFullNestedDTO(GetCoursesDTO):
    lessons: list["GetLessonNestedExercisesDTO"]
    exercises: list["GetExercisesDTO"]


class GetNestedCoursesDTO(GetCoursesDTO):
    lessons: list["GetLessonsDTO"]
    exercises: list["GetExercisesDTO"]


class CreateCoursesDTO(BaseModel):
    title: str


class UpdateCoursesDTO(BaseModel):
    title: Optional[str] = None


class UpdateCourseRelationDTO(UpdateTaskRelationDTOBase):
    pass
