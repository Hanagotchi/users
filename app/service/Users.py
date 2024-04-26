from exceptions.UserException import UserNotFound, InvalidData, InvalidURL
from exceptions.LoginException import AuthenticationError
from models.users import User
from repository.Users import UsersRepository
import requests
import os
import re
import jwt
import uuid

TOKEN_FIELD_NAME = "x-access-token"


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

    def get_users_by_ids(self, ids: list):
        return self.user_repository.get_users_by_ids(ids)

    def create_user(self, user_data: dict):
        if not self._validate_location(user_data.get("location")):
            raise InvalidData()
        try:
            user = self.user_repository.create_user(**user_data)
            return user
        except Exception as e:
            self.user_repository.rollback()
            raise e

    def update_user(self, user_id: int, update_data: dict):
        self.get_user(user_id)
        filtered_update_data = {k: v for k, v in update_data.items()
                                if v is not None}
        if 'photo' in filtered_update_data:
            photo_url = filtered_update_data['photo']
            if not re.match(r'^https?://(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}'
                            r'(?:/[^/#?]+)+(?:\?.*)?$', photo_url):
                raise InvalidURL("Invalid photo URL")
        try:
            self.user_repository.edit_user(user_id, filtered_update_data)
        except Exception as e:
            self.user_repository.rollback()
            raise e

    def _generate_nickname(self, name):

        name_without_spaces = name.replace(" ", "")
        uuid_max = 8
        max_length = 18
        random_uuid = str(uuid.uuid4()).replace("-", "")[:uuid_max]
        truncated_name = name_without_spaces[:(max_length - uuid_max)]
        nickname = truncated_name + random_uuid

        return nickname

    def login(self, auth_code: str):
        access_token = self._get_access_token(auth_code)
        if access_token is None:
            raise AuthenticationError("Authentication code is invalid")

        user_info = self._get_user_info(access_token)
        user = self.user_repository.get_user_by_email(user_info["email"])

        if user is None:
            print(f"user info: {user_info}")
            if "name" in user_info:
                name = user_info["name"]
            else:
                email = user_info["email"]
                match = re.match(r"([^@]+)@.*", email)
                if match:
                    name = match.group(1)
            nickname = self._generate_nickname(name)
            user_info["nickname"] = nickname
            self.user_repository.add(User(**user_info))
            user = self.user_repository.get_user_by_email(user_info["email"])
        user_id = user.get("id")
        payload = {"user_id": user_id}
        jwt_token = jwt.encode(payload,
                               os.environ["JWT_SECRET"],
                               algorithm="HS256")
        return user, jwt_token

    def _get_access_token(self, authorization_code):
        token_url = "https://oauth2.googleapis.com/token"
        payload = {
            "client_id": os.environ["GOOGLE_CLIENT_ID"],
            "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
            "code": authorization_code,
            "grant_type": "authorization_code",
            "redirect_uri": os.environ["GOOGLE_REDIRECT_URI"],
        }
        response = requests.post(token_url, data=payload)
        if response.status_code == 200:
            return response.json().get("access_token")
        else:
            return None

    def _get_user_info(self, access_token):
        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        params = {"fields": "id,email,name,picture,gender"}
        response = requests.get(user_info_url, headers=headers, params=params)

        if response.status_code != 200:
            raise AuthenticationError()

        user_data = {"email": response.json().get("email")}
        if response.json().get("gender") is not None:
            user_data["gender"] = response.json().get("gender")
        if response.json().get("name") is not None:
            user_data["name"] = response.json().get("name")
        if response.json().get("picture") is not None:
            user_data["photo"] = response.json().get("picture")
        return user_data

    def _validate_location(self, location):
        if "lat" in location and "long" in location:
            if -90 <= location["lat"] <= 90 and -180 \
                   <= location["long"] <= 180:
                return True
        return False

    def retrieve_user_id(self, request):
        token = self.__get_token(request.headers)
        payload = jwt.decode(token,
                             os.environ["JWT_SECRET"],
                             algorithms=["HS256"])
        return int(payload.get("user_id"))

    def __get_token(self, headers: dict):
        keyName = None
        for key in headers.keys():
            if key.lower() == TOKEN_FIELD_NAME:
                keyName = key
        if not keyName:
            return None
        return headers.get(keyName)
