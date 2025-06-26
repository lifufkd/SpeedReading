from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base_mixins import TimestampMixin
from src.database.base import OrmBase


class ExercisesLessons(OrmBase, TimestampMixin):
    __tablename__ = 'exercises_lessons'
    exercise_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("exercises.exercise_id", ondelete="CASCADE"),
        primary_key=True
    )
    lesson_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("lessons.lesson_id", ondelete="CASCADE"),
        primary_key=True
    )


class ExercisesCourses(OrmBase, TimestampMixin):
    __tablename__ = 'exercises_courses'
    exercise_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("exercises.exercise_id", ondelete="CASCADE"),
        primary_key=True
    )
    course_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("courses.course_id", ondelete="CASCADE"),
        primary_key=True
    )


class LessonsCourses(OrmBase, TimestampMixin):
    __tablename__ = 'lessons_courses'
    lesson_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("lessons.lesson_id", ondelete="CASCADE"),
        primary_key=True
    )
    course_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("courses.course_id", ondelete="CASCADE"),
        primary_key=True
    )
