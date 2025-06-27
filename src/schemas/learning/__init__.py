from src.schemas.learning.exercise import ExerciseNestedSchema, ExerciseSchema
from src.schemas.learning.courses import CoursesNestedSchema, CoursesSchema
from src.schemas.learning.lessons import LessonsNestedSchema, LessonsSchema

ExerciseNestedSchema.model_rebuild()
CoursesNestedSchema.model_rebuild()
LessonsNestedSchema.model_rebuild()
