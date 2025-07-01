from src.dto.lessons import GetNestedLessonsDTO, GetLessonNestedExercisesDTO, GetLessonsDTO
from src.dto.exercises import GetNestedExercisesDTO, GetExercisesDTO
from src.dto.courses import GetNestedCoursesDTO, GetCourseFullNestedDTO, GetCoursesDTO
from src.dto.assignment import UsersTasksDTO, UsersProgressDTO # noqa
from src.dto.users import GetUserNestedTasksDTO, GetUserNestedProgressDTO, GetUserNestedDTO
from src.dto.tasks import GetUserTaskTreeDTO

GetNestedLessonsDTO.model_rebuild()
GetNestedExercisesDTO.model_rebuild()
GetNestedCoursesDTO.model_rebuild()
GetUserNestedTasksDTO.model_rebuild()
GetUserNestedProgressDTO.model_rebuild()
GetUserNestedDTO.model_rebuild()
GetLessonNestedExercisesDTO.model_rebuild()
GetCourseFullNestedDTO.model_rebuild()
GetUserTaskTreeDTO.model_rebuild()
