from fastapi import HTTPException, status
from typing import Optional


class AuthenticationError(HTTPException):
    def __init__(self, message: Optional[str] = "Could not authenticate"):
        status_code = status.HTTP_401_UNAUTHORIZED
        super().__init__(status_code=status_code, detail=message)
