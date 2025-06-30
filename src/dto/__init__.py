from src.dto.lessons import GetNestedLessonsDTO, GetLessonsDTO
from src.dto.exercises import GetNestedExercisesDTO, GetExercisesDTO
from src.dto.courses import GetNestedCoursesDTO, GetCoursesDTO
from src.dto.assignment import UsersTasksDTO, UsersProgressDTO # noqa
from src.dto.users import GetUserNestedTasksDTO, GetUserNestedProgressDTO, GetUserNestedDTO

GetNestedLessonsDTO.model_rebuild()
GetNestedExercisesDTO.model_rebuild()
GetNestedCoursesDTO.model_rebuild()
GetUserNestedTasksDTO.model_rebuild()
GetUserNestedProgressDTO.model_rebuild()
GetUserNestedDTO.model_rebuild()
