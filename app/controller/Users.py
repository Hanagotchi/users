from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from service.Social import SocialService
from service.Users import UsersService


class UsersController:
    def __init__(self, users_service: UsersService):
        self.users_service = users_service

    def handle_get_user(self, user_id: int):
        user = self.users_service.get_user(user_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(
                {
                    "message": user,
                    "status": status.HTTP_200_OK,
                }
            ),
        )

    def handle_get_all_users(self, ids: list = None):
        if ids:
            users = self.users_service.get_users_by_ids(ids)
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=jsonable_encoder(
                    {
                        "message": users,
                        "status": status.HTTP_200_OK,
                    }
                ),
            )
        else:
            users = self.users_service.get_all_users()
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=jsonable_encoder(
                    {
                        "message": users,
                        "status": status.HTTP_200_OK,
                    }
                ),
            )

    async def handle_create_user(self, user_data: dict):
        result = self.users_service.create_user(user_data)
        await SocialService.create_social_user(user_id=result.id)
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content=jsonable_encoder(
                {
                    "message": "User created successfully",
                    "status": status.HTTP_201_CREATED,
                }
            ),
        )

    async def handle_login(self, auth_code: str):
        user, jwt_token = self.users_service.login(auth_code)
        await SocialService.create_social_user(user_id=user.get("id"))
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content=jsonable_encoder(
                {
                    "message": user,
                    "status": status.HTTP_200_OK,
                }
            ),
            headers={"x-access-token": f"{jwt_token}"},
        )

    def handle_update_user(self, user_id: int, update_data: dict):
        self.users_service.update_user(user_id, update_data)
        return {
            "message": "User updated successfully",
            "status": status.HTTP_200_OK,
        }
