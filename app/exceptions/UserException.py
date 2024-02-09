from fastapi import status


class UsersException(Exception):
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code


class UserNotFound(UsersException):
    def __init__(self, id: int):
        super().__init__(f"User with id {id} not found",
                         status.HTTP_404_NOT_FOUND)
