from src.dto.learning.lessons import GetNestedLessonsDTO, GetLessonsDTO
from src.dto.learning.exercises import GetNestedExercisesDTO, GetExercisesDTO
from src.dto.learning.courses import GetNestedCoursesDTO, GetCoursesDTO

GetNestedLessonsDTO.model_rebuild()
GetNestedExercisesDTO.model_rebuild()
GetNestedCoursesDTO.model_rebuild()
