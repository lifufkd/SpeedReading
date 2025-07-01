from src.dto.learning.exercises import GetExercisesDTO # noqa
from src.dto.learning.lessons import GetLessonNestedExercisesDTO
from src.dto.learning.courses import GetCourseFullNestedDTO
from src.dto.student.tasks import GetUserTaskTreeDTO

GetLessonNestedExercisesDTO.model_rebuild()
GetCourseFullNestedDTO.model_rebuild()
GetUserTaskTreeDTO.model_rebuild()
