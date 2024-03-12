from fastapi import status
from service.Users import UsersService


class UsersController:
    def __init__(self, users_service: UsersService):
        self.users_service = users_service

    def handle_get_user(self, user_id: int):
        user = self.users_service.get_user(user_id)
        return {"message": user, "status": status.HTTP_200_OK}

    def handle_get_all_users(self):
        users = self.users_service.get_all_users()
        return {"users": users, "status": status.HTTP_200_OK}

    def handle_create_user(self, user_data: dict):
        self.users_service.create_user(user_data)
        return {
            "message": "User created successfully",
            "status": status.HTTP_201_CREATED,
        }

    def handle_login(self, auth_code: str):
        user = self.users_service.login(auth_code)
        return {
            "message": user,
            "status": status.HTTP_200_OK,
        }
