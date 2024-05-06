from fastapi import Depends, FastAPI, Query
from controller.Users import UsersController
from service.Users import UsersService
from repository.Users import UsersRepository
from typing import List, Annotated, Union
from schemas.Schemas import (
    CreateUserSchema,
    UpdateUserSchema,
    LoginRequest,
    CreateNotificationSchema
)
from security.JWTBearer import get_current_user_id
from logs import init_logging
logger = init_logging('user-repository')

app = FastAPI()
users_repository = UsersRepository()
users_service = UsersService(users_repository)
users_controller = UsersController(users_service)


@app.get("/")
def root():
    return {"message": "users service"}


@app.get("/users/me")
def get_users(user_id: Annotated[int, Depends(get_current_user_id)]):
    return users_controller.handle_get_user(user_id)


@app.get("/users")
def get_all_users(_: Annotated[int, Depends(get_current_user_id)],
                  ids: Annotated[Union[List[str], None], Query()] = None):
    return users_controller.handle_get_all_users(ids)


@app.post("/users")
async def create_user(user_data: CreateUserSchema):
    return await users_controller.handle_create_user(user_data.dict())


@app.post("/login")
async def login_with_google(request: LoginRequest):
    return await users_controller.handle_login(request.auth_code)


@app.patch("/users/me")
async def update_user(update_data: UpdateUserSchema,
                      user_id: Annotated[int, Depends(get_current_user_id)]):
    return users_controller.handle_update_user(update_data.dict(), user_id)


@app.post("/users/me/notification")
async def create_notification(
    user_id: Annotated[int,
                       Depends(get_current_user_id)],
    create_notification: CreateNotificationSchema
):
    logger.info(f"Creating notification for user {user_id}")
    return users_controller.handle_create_notification(
        create_notification.dict(), user_id)
