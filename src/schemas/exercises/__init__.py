from src.schemas.exercises.exercise import ExerciseNestedSchema, ExerciseSchema
from src.schemas.exercises.courses import CoursesNestedSchema, CoursesSchema
from src.schemas.exercises.lessons import LessonsNestedSchema, LessonsSchema

ExerciseNestedSchema.model_rebuild()
CoursesNestedSchema.model_rebuild()
LessonsNestedSchema.model_rebuild()
