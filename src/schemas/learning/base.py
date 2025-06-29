from pydantic import BaseModel, model_validator

from src.validators.common_schemas import validate_at_least_one_filled, ensure_no_duplicates_across_fields


class UniqueFieldValidator(BaseModel):
    @model_validator(mode='after')
    def validate_model(cls, model):
        data = model.model_dump()
        validate_at_least_one_filled(data)
        ensure_no_duplicates_across_fields(data)
        return model
