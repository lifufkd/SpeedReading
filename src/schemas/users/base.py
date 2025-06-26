from pydantic import BaseModel, field_validator, EmailStr
from typing import Optional
from datetime import datetime

from src.validators.users_schemas import validate_password_strength
from src.schemas.enums import UsersRoles


class UserSchemaBase(BaseModel):
    user_id: int
    login: str
    email: Optional[EmailStr]
    role: UsersRoles
    created_at: datetime
    updated_at: datetime


class PasswordValidatorBase(BaseModel):
    @field_validator("password", check_fields=False)
    @classmethod
    def check_password(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            validate_password_strength(value)
        return value
