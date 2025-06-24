from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional, Annotated

from src.validators.users_schemas import validate_password_strength


class UpdateProfileSchema(BaseModel):
    login: Annotated[Optional[str], Field(None, min_length=3, max_length=64)]
    password: Optional[str] = None
    email: Optional[EmailStr] = None

    @field_validator("password", check_fields=False)
    @classmethod
    def check_password(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            validate_password_strength(value)
        return value


class UpdateProfileDTO(UpdateProfileSchema):
    password_hash: Optional[str] = None
