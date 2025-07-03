from pydantic import BaseModel, model_validator, Field

from src.validators.common_schemas import validate_at_least_one_filled, ensure_no_duplicates_across_fields
from src.schemas.enums import TaskTypes


class UniqueFieldValidator(BaseModel):
    @model_validator(mode='after')
    def validate_model(cls, model):
        data = model.model_dump()
        validate_at_least_one_filled(data)
        ensure_no_duplicates_across_fields(data)
        return model


class UpdateTaskRelationSchemaBase(UniqueFieldValidator):
    task_type: TaskTypes
    add_ids: list[int] = Field(default_factory=list)
    delete_ids: list[int] = Field(default_factory=list)
