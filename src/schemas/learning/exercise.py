from pydantic import BaseModel, model_validator
from typing import Optional
from datetime import datetime

from src.validators.common_schemas import validate_at_least_one_filled, ensure_no_duplicates_across_fields
from src.schemas.enums import ExerciseTypes


class ExerciseSchema(BaseModel):
    exercise_id: int
    title: str
    type: ExerciseTypes
    created_at: datetime
    updated_at: datetime


class ExerciseNestedSchema(ExerciseSchema):
    lessons: list["LessonsSchema"]
    courses: list["CoursesSchema"]


class CreateExerciseSchema(BaseModel):
    title: str
    type: ExerciseTypes


class UpdateExerciseSchema(BaseModel):
    title: Optional[str] = None
    type: Optional[ExerciseTypes] = None


class UpdateExerciseLessonsSchema(BaseModel):
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


class UpdateExerciseCoursesSchema(BaseModel):
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
