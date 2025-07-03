from pydantic import BaseModel
from typing import Optional

from src.dto.base import TimestampedDTO
from src.schemas.enums import TaskTypes
from src.dto.learning.base import UpdateTaskRelationDTOBase


class GetLessonsDTO(TimestampedDTO):
    lesson_id: int
    title: str


class GetLessonNestedExercisesDTO(GetLessonsDTO):
    exercises: list["GetExercisesDTO"]


class GetNestedLessonsDTO(GetLessonsDTO):
    exercises: list["GetExercisesDTO"]
    courses: list["GetCoursesDTO"]


class CreateLessonsDTO(BaseModel):
    title: str


class UpdateLessonsDTO(BaseModel):
    title: Optional[str] = None


class UpdateLessonRelationDTO(UpdateTaskRelationDTOBase):
    pass
