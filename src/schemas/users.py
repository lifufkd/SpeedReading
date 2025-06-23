from pydantic import BaseModel, Field, field_validator
from typing import Annotated, Optional

from src.schemas.enums import UsersRoles
from src.validators.users_schemas import validate_password_strength


class GetUserSchema(BaseModel):
    user_id: int
    login: str
    role: UsersRoles

    class Config:
        from_attributes = True


class UserSchema(GetUserSchema):
    password_hash: str


class CreateUserSchema(BaseModel):
    login: Annotated[str, Field(min_length=3, max_length=64)]
    password: str
    role: UsersRoles

    @field_validator("password")
    @classmethod
    def check_password(cls, value: str) -> str:
        validate_password_strength(value)
        return value


class CreateUserDTO(BaseModel):
    login: Annotated[str, Field(min_length=3, max_length=64)]
    password_hash: str
    role: UsersRoles


class UpdateUserSchema(BaseModel):
    user_id: int
    login: Annotated[Optional[str], Field(None, min_length=3, max_length=64)]
    password: Optional[str] = None
    role: Optional[UsersRoles] = None

    @field_validator("password", check_fields=False)
    @classmethod
    def check_password(cls, value: Optional[str]) -> Optional[str]:
        if value is not None:
            validate_password_strength(value)
        return value


class UpdateUserDTO(BaseModel):
    user_id: int
    login: Annotated[Optional[str], Field(None, min_length=3, max_length=64)]
    password_hash: Optional[str] = None
    role: Optional[UsersRoles] = None

