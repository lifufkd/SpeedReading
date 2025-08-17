from pydantic import BaseModel, model_validator, Field

from src.validators.common_schemas import validate_non_empty, validate_no_duplicates
from src.schemas.enums import TaskTypes


class UniqueFieldValidator(BaseModel):
    @model_validator(mode='after')
    def validate_lists_non_empty(self):
        return validate_non_empty(self)

    @model_validator(mode='after')
    def validate_lists_no_duplicates(self):
        return validate_no_duplicates(self)


class UpdateTaskRelationSchemaBase(UniqueFieldValidator):
    type: TaskTypes
    add_ids: list[int] = Field(default_factory=list)
    delete_ids: list[int] = Field(default_factory=list)
