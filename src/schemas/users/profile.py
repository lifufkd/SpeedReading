from pydantic import EmailStr, Field
from typing import Optional

from src.schemas.users.base import UserSchemaBase
from src.schemas.users.base import PasswordValidatorBase


class UserSchema(UserSchemaBase):
    pass


class UpdateProfileSchema(PasswordValidatorBase):
    login: Optional[str] = Field(None, min_length=3, max_length=64)
    password: Optional[str] = None
    email: Optional[EmailStr] = None
