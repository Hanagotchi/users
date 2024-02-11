from fastapi import HTTPException, status


class UserNotFound(HTTPException):
    def __init__(self, id: int):
        status_code = status.HTTP_404_NOT_FOUND
        detail = f"User with id {id} not found"
        super().__init__(status_code=status_code, detail=detail)
