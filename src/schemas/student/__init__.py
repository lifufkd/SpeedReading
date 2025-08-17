from src.schemas.learning.exercise import ExerciseSchema # noqa
from src.schemas.learning.lessons import LessonNestedExercisesSchema
from src.schemas.learning.courses import CourseFullNestedSchema
from src.schemas.student.tasks import UserTaskTreeSchema

LessonNestedExercisesSchema.model_rebuild()
CourseFullNestedSchema.model_rebuild()
UserTaskTreeSchema.model_rebuild()
