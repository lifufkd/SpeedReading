from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy import Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column

from src.database.base_mixins import TimestampMixin
from src.database.base import OrmBase
from src.schemas.enums import ExerciseCompleteStatus


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


class UsersExercisesStatus(OrmBase, TimestampMixin):
    __tablename__ = 'users_exercises_status'
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        primary_key=True
    )
    exercise_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("exercises.exercise_id", ondelete="CASCADE"),
        primary_key=True
    )
    status: Mapped[ExerciseCompleteStatus] = mapped_column(
        SAEnum(ExerciseCompleteStatus, name="users_exercises_status_status_enum", create_constraint=True),
        nullable=False,
        default=ExerciseCompleteStatus.NOT_STARTED
    )
