from exceptions.UserException import UserNotFound
from repository.Users import UsersRepository
# from repository.UsersLocal import UsersRepository


class UsersService:
    def __init__(self, user_repository: UsersRepository):
        self.user_repository = user_repository

    def get_user(self, user_id: int):
        user = self.user_repository.get_user(user_id)
        if not user:
            raise UserNotFound(user_id)
        return user

    def get_all_users(self):
        return self.user_repository.get_all_users()

    def create_user(self, user_data: dict):
        name = user_data.get("name")
        return self.user_repository.create_user(name)
