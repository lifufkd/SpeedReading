from fastapi import status


class AppException(Exception):
    def __init__(self, detail: str, status_code: int = status.HTTP_400_BAD_REQUEST):
        self.detail = detail
        self.status_code = status_code


class UserNotFound(AppException):
    def __init__(self):
        super().__init__(detail="User not found", status_code=404)


class UserAlreadyExists(AppException):
    def __init__(self):
        super().__init__(detail="User already existed", status_code=409)


class UserIsNotAdmin(AppException):
    def __init__(self):
        super().__init__(detail="User is not admin", status_code=403)


class UserIdIsSame(AppException):
    def __init__(self):
        super().__init__(detail="Your id and requested are same, this not allowed", status_code=422)
