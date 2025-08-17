from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base_mixins import TimestampMixin
from src.database.base import OrmBase


class Lessons(OrmBase, TimestampMixin):
    __tablename__ = 'lessons'
    lesson_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)

    exercises: Mapped[list["Exercises"]] = relationship(
        back_populates="lessons",
        secondary="exercises_lessons"
    )
    courses: Mapped[list["Courses"]] = relationship(
        back_populates="lessons",
        secondary="lessons_courses"
    )

    def __repr__(self):
        return f"<Lesson(lesson_id='{self.lesson_id}', title='{self.title}')>"
