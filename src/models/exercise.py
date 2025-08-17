from sqlalchemy import BigInteger
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base_mixins import TimestampMixin
from src.database.base import OrmBase
from src.schemas.enums import ExerciseTypes


class Exercises(OrmBase, TimestampMixin):
    __tablename__ = 'exercises'
    exercise_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[ExerciseTypes] = mapped_column(
        SAEnum(ExerciseTypes, name="exercises_type_enum", create_constraint=True),
        nullable=False
    )

    lessons: Mapped[list["Lessons"]] = relationship(
        back_populates="exercises",
        secondary="exercises_lessons"
    )
    courses: Mapped[list["Courses"]] = relationship(
        back_populates="exercises",
        secondary="exercises_courses"
    )

    def __repr__(self):
        return f"<Exercises(exercise_id='{self.exercise_id}', title='{self.title}', type='{self.type}')>"
