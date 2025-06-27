from pydantic import BaseModel, model_validator
from typing import Optional
from datetime import datetime

from src.validators.common_schemas import validate_at_least_one_filled, ensure_no_duplicates_across_fields


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
    add_exercises_ids: Optional[list[int]] = []
    delete_exercises_ids: Optional[list[int]] = []

    @model_validator(mode='after')
    def validate_at_least_one(cls, model):
        validate_at_least_one_filled(model.model_dump())
        return model

    @model_validator(mode="after")
    def validate_no_duplicates_across_fields(cls, model):
        ensure_no_duplicates_across_fields(model.model_dump())
        return model


class UpdateCoursesLessonsSchema(BaseModel):
    add_lessons_ids: Optional[list[int]] = []
    delete_lessons_ids: Optional[list[int]] = []

    @model_validator(mode='after')
    def validate_at_least_one(cls, model):
        validate_at_least_one_filled(model.model_dump())
        return model

    @model_validator(mode="after")
    def validate_no_duplicates_across_fields(cls, model):
        ensure_no_duplicates_across_fields(model.model_dump())
        return model
