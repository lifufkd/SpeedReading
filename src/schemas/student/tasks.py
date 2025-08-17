from pydantic import BaseModel


class UserTaskTreeSchema(BaseModel):
    courses: list["CourseFullNestedSchema"] | list = []
    lessons: list["LessonNestedExercisesSchema"] | list = []
    exercises: list["ExerciseSchema"] | list = []
