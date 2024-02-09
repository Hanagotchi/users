from fastapi import status
from service.Users import UsersService


class UsersController:
    def __init__(self, users_service: UsersService):
        self.users_service = users_service

    def handle_get_user(self, user_id: int):
        user = self.users_service.get_user(user_id)
        return {"message": user, "status": status.HTTP_200_OK}
