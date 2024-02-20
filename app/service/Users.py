from exceptions.UserException import UserNotFound
from repository.Users import UsersRepository
import requests
import os


def get_access_token(authorization_code):
    token_url = "https://oauth2.googleapis.com/token"
    payload = {
        "client_id": os.environ["GOOGLE_CLIENT_ID"],
        "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
        "code": authorization_code,
        "grant_type": "authorization_code",
        "redirect_uri": "http://localhost:8000/auth/google/callback"
    }
    response = requests.post(token_url, data=payload)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        return None


def get_user_info(access_token):
    user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
    headers = {"Authorization": f"Bearer {access_token}"}
    params = {"fields": "id,email,name,picture"}
    response = requests.get(user_info_url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None


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
        mail = user_data.get("mail")
        return self.user_repository.create_user(name, mail)

    def login(self, auth_code: str):
        access_token = get_access_token(auth_code)
        user_info = get_user_info(access_token)

        user = self.user_repository.get_user_by_name(user_info["email"])
        if user is None:
            user = self.user_repository.create_user(user_info["email"])

        return user
