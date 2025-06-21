from pydantic import BaseModel

from src.schemas.enums import UsersRoles


class UserSchema(BaseModel):
    users_id: int
    login: str
    password_hash: str
    role: UsersRoles

    class Config:
        from_attributes = True
