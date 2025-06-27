from src.dto.lessons import GetNestedLessonsDTO, GetLessonsDTO
from src.dto.exercises import GetNestedExercisesDTO, GetExercisesDTO
from src.dto.courses import GetNestedCoursesDTO, GetCoursesDTO

GetNestedLessonsDTO.model_rebuild()
GetNestedExercisesDTO.model_rebuild()
GetNestedCoursesDTO.model_rebuild()
