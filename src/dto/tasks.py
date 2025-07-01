from pydantic import BaseModel


class GetUserTaskTreeDTO(BaseModel):
    courses: list["GetCourseFullNestedDTO"] | list = []
    lessons: list["GetLessonNestedExercisesDTO"] | list = []
    exercises: list["GetExercisesDTO"] | list = []
