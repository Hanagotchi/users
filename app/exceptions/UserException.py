from fastapi import HTTPException, status


class UserNotFound(HTTPException):
    def __init__(self, id: int):
        status_code = status.HTTP_404_NOT_FOUND
        detail = f"User with id {id} not found"
        super().__init__(status_code=status_code, detail=detail)


class InvalidData(HTTPException):
    def __init__(self):
        status_code = status.HTTP_400_BAD_REQUEST
        super().__init__(
            status_code=status_code, detail="Invalid user data was provided"
        )


class InvalidURL(HTTPException):
    def __init__(self, detail: str):
        status_code = status.HTTP_400_BAD_REQUEST
        super().__init__(status_code=status_code, detail=detail)


class ForbiddenUser(HTTPException):
    def __init__(self):
        status_code = status.HTTP_403_FORBIDDEN
        detail = "User is not authorized"
        super().__init__(status_code=status_code, detail=detail)


class UnauthorizedUser(HTTPException):
    def __init__(self):
        status_code = status.HTTP_401_UNAUTHORIZED
        detail = "Invalid credentials"
        super().__init__(status_code=status_code, detail=detail)
