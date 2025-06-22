from sqlalchemy import BigInteger
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base import OrmBase
from src.schemas.enums import UsersRoles


class Users(OrmBase):
    __tablename__ = 'users'
    users_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    login: Mapped[str] = mapped_column(nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    role: Mapped[UsersRoles] = mapped_column(
        SAEnum(UsersRoles, name="users_role_enum", create_constraint=True),
        nullable=False
    )

    def __repr__(self):
        return f"<User(id={self.users_id}, login='{self.login}', password_hash='{self.password_hash}', role='{self.role}')>"
