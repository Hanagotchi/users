from exceptions.UserException import UserNotFound, InvalidData
from exceptions.LoginException import AuthenticationError
from models.users import User
from repository.Users import UsersRepository
import requests
import os


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
        email = user_data.get("email")
        if (not self._validate_location(user_data.get("location"))):
            raise InvalidData()
        return self.user_repository.create_user(**user_data)

    def login(self, auth_code: str):
        access_token = self._get_access_token(auth_code)
        if access_token is None:
            raise AuthenticationError("Authentication code is invalid")

        user_info = self._get_user_info(access_token)
        user = self.user_repository.get_user_by_email(user_info["email"])

        if user is None:
            self.user_repository.add(User(**user_info))
            user = self.user_repository.get_user_by_email(user_info["email"])

        return user

    def update_user(self, user_id: int, update_data: dict):
        # TODO: aca habria que chequear a partir del token, session o algo que
        # es el propio usuario editando sus datos y no permitir
        # que un usuario edite los de un tercero
        self.get_user(user_id)
        self.user_repository.edit_user(user_id, update_data)

    def _get_access_token(self, authorization_code):
        token_url = "https://oauth2.googleapis.com/token"
        payload = {
            "client_id": os.environ["GOOGLE_CLIENT_ID"],
            "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
            "code": authorization_code,
            "grant_type": "authorization_code",
            "redirect_uri": os.environ["GOOGLE_REDIRECT_URI"]
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

        user_data = {'email': response.json().get("email")}
        if response.json().get("gender") is not None:
            user_data['gender'] = response.json().get("gender")
        if response.json().get("name") is not None:
            user_data['name'] = response.json().get("name")
        if response.json().get("picture") is not None:
            user_data['photo'] = response.json().get("picture")
        return user_data

    def _validate_location(self, location):
        if "lat" in location and "long" in location:
            latitud = location["lat"]
            longitud = location["long"]

            if (-90<=location["lat"]<= 90 and -180<=location["long"]<= 180):
                return True

            return False

"""             if isinstance(latitud, (int, float)) and isinstance(longitud, (int, float)):
                if -90 <= latitud <= 90 and -90 <= longitud <= 90:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False """

