from pydantic import BaseModel, model_validator
from typing import Optional
from datetime import datetime

from src.validators.common_schemas import validate_at_least_one_filled, ensure_no_duplicates_across_fields


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


class UpdateLessonsCoursesSchema(BaseModel):
    add_courses_ids: Optional[list[int]] = []
    delete_courses_ids: Optional[list[int]] = []

    @model_validator(mode='after')
    def validate_at_least_one(cls, model):
        validate_at_least_one_filled(model.model_dump())
        return model

    @model_validator(mode="after")
    def validate_no_duplicates_across_fields(cls, model):
        ensure_no_duplicates_across_fields(model.model_dump())
        return model
