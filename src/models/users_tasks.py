from sqlalchemy import BigInteger, ForeignKey, UniqueConstraint
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base_mixins import TimestampMixin
from src.database.base import OrmBase
from src.schemas.enums import TaskTypes


class UsersTasks(OrmBase, TimestampMixin):
    __tablename__ = 'users_tasks'
    users_tasks_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey('users.user_id', ondelete='CASCADE'),
        index=True
    )
    task_id: Mapped[int] = mapped_column(
        BigInteger,
        nullable=False,
        index=True
    )
    task_type: Mapped[TaskTypes] = mapped_column(
        SAEnum(TaskTypes, name="users_tasks_task_type_enum", create_constraint=True),
        nullable=False
    )

    user: Mapped["Users"] = relationship(back_populates="tasks")

    __table_args__ = (
        UniqueConstraint(
            "user_id", "task_id", "task_type",
            name="users_tasks_user_id_task_id_task_type"
        ),
    )

    def __repr__(self):
        return (f"<UsersTasks("
                f"users_tasks_id='{self.users_tasks_id}', "
                f"user_id='{self.user_id}', "
                f"task_id='{self.task_id}', "
                f"task_type='{self.task_type}')>")
