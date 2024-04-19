import jwt
import os
from exceptions.UserException import ForbiddenUser, UnauthorizedUser


TOKEN_FIELD_NAME = "x-access-token"


class AuthService():
    def __init__(self):
        self.__secret = os.environ.get("JWT_SECRET")

    def authenticate(self, user_id: int, request):
        token = self._get_token(request.headers)
        if not token:
            raise UnauthorizedUser()
        try:
            payload = jwt.decode(token, self.__secret, algorithms=["HS256"])

        except jwt.ExpiredSignatureError:
            raise UnauthorizedUser()

        except jwt.InvalidTokenError:
            raise UnauthorizedUser()

        if payload.get("user_id") != user_id:
            raise ForbiddenUser()

        return

    def _get_token(self, headers: dict):
        keyName = None
        for key in headers.keys():
            if key.lower() == TOKEN_FIELD_NAME:
                keyName = key
        if not keyName:
            return None
        return headers.get(keyName)
