from src.dto.lessons import GetNestedLessonsDTO, GetLessonsDTO
from src.dto.exercises import GetNestedExercisesDTO, GetExercisesDTO
from src.dto.courses import GetNestedCoursesDTO, GetCoursesDTO
from src.dto.assignment import AssignmentDTO # noqa
from src.dto.users import GetNestedUsersDTO

GetNestedLessonsDTO.model_rebuild()
GetNestedExercisesDTO.model_rebuild()
GetNestedCoursesDTO.model_rebuild()
GetNestedUsersDTO.model_rebuild()
