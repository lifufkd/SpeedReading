from fastapi import status


class AppException(Exception):
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST, headers: dict | None = None):
        self.detail = detail
        self.status_code = status_code
        self.headers = headers


class UserNotFound(AppException):
    def __init__(self):
        super().__init__(detail="User not found", status_code=404)


class UserAlreadyExists(AppException):
    def __init__(self, user_id: int | None = None, user_name: str | None = None):
        if user_id and user_name:
            msg = f"User with id({user_id}) and username({user_name}) already exists.)"
        elif user_id:
            msg = f"User with id({user_id}) already exists."
        elif user_name:
            msg = f"User with username({user_name}) already exists."
        else:
            msg = "User already existed"
        super().__init__(detail=msg, status_code=409)


class UserIsNotAdmin(AppException):
    def __init__(self):
        super().__init__(detail="User is not admin", status_code=403)


class UserIdIsSame(AppException):
    def __init__(self):
        super().__init__(detail="Your id and requested are same, this not allowed", status_code=422)


class JWTError(AppException):
    def __init__(self):
        super().__init__(detail="Invalid or expired JWT token", status_code=401, headers={"WWW-Authenticate": "Bearer"})


class ExerciseNotFound(AppException):
    def __init__(self):
        super().__init__(detail="Exercise not found", status_code=404)


class LessonsNotFound(AppException):
    def __init__(self, lessons_ids: list[int]):
        super().__init__(detail=f"Lessons with ids:({','.join(map(str, lessons_ids))}) not found", status_code=404)


class CoursesNotFound(AppException):
    def __init__(self, courses_ids: list[int]):
        super().__init__(detail=f"Courses with ids:({','.join(map(str, courses_ids))}) not found", status_code=404)
