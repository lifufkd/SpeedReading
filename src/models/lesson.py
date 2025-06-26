from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base_mixins import TimestampMixin
from src.database.base import OrmBase


class Lessons(OrmBase, TimestampMixin):
    __tablename__ = 'lessons'
    lesson_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)

    exercises: Mapped[list["Exercises"]] = relationship(
        secondary="exercises_lessons"
    )

    def __repr__(self):
        return f"<Lesson(lesson_id='{self.lesson_id}', title='{self.title}')>"
