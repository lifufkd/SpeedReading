from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database.base_mixins import TimestampMixin
from src.database.base import OrmBase


class Courses(OrmBase, TimestampMixin):
    __tablename__ = 'courses'
    course_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)

    lessons: Mapped[list["Lessons"]] = relationship(
        secondary="lessons_courses"
    )
    exercises: Mapped[list["Exercises"]] = relationship(
        secondary="exercises_courses"
    )

    def __repr__(self):
        return f"<Courses(course_id='{self.course_id}', title='{self.title}')>"
