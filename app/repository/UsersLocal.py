from schemas.Schemas import UserSchema


class UsersRepository:
    def __init__(self):
        self.db = {}
        self._populate_default_users()

    def _populate_default_users(self):
        default_users_data = [
            {"id": 1, "name": "John"},
            {"id": 2, "name": "Alice"},
            {"id": 3, "name": "Bob"},
        ]
        for user_data in default_users_data:
            user = UserSchema(**user_data)
            self.db[user.id] = user

    def get_user(self, user_id):
        return self.db.get(user_id)

    def get_all_users(self):
        return list(self.db.values())

    def create_user(self, name: str):
        new_user_id = max(self.db.keys()) + 1
        new_user = UserSchema(id=new_user_id, name=name)
        self.db[new_user_id] = new_user
        return new_user
