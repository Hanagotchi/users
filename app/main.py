from fastapi import Depends, FastAPI, Query
from controller.Users import UsersController
from service.Users import UsersService
from repository.Users import UsersRepository
from typing import List, Annotated, Union
from schemas.Schemas import (
    CreateUserSchema,
    UpdateUserSchema,
    LoginRequest,
    CreateNotificationSchema,
    UpdateNotificationSchema
)
from security.JWTBearer import get_current_user_id


app = FastAPI(
    title="Users API",
    version="0.1.0",
    summary="Microservice for users management",
)

users_repository = UsersRepository()
users_service = UsersService(users_repository)
users_controller = UsersController(users_service)


@app.get("/", tags=["Healthcheck"])
def root():
    return {"message": "users service"}


@app.get("/users/{user_id}", tags=["Users"])
def get_users(user_id: int):
    return users_controller.handle_get_user(user_id)


@app.get("/users", tags=["Users"])
def get_all_users(ids: Annotated[Union[List[str], None], Query()] = None):
    return users_controller.handle_get_all_users(ids)


@app.post("/users", tags=["Users"])
async def create_user(user_data: CreateUserSchema):
    return await users_controller.handle_create_user(user_data.dict())


@app.post("/login", tags=["Auth"])
async def login_with_google(request: LoginRequest):
    return await users_controller.handle_login(request.auth_code)


@app.patch("/users/me", tags=["Users"])
async def update_user(update_data: UpdateUserSchema,
                      user_id: Annotated[int, Depends(get_current_user_id)]):
    return users_controller.handle_update_user(update_data.dict(), user_id)


@app.post("/users/me/notification", tags=["Notifications"])
async def create_notification(
    user_id: Annotated[int,
                       Depends(get_current_user_id)],
    create_notification: CreateNotificationSchema
):
    return users_controller.handle_create_notification(
        create_notification.dict(), user_id)


@app.get("/users/me/notifications", tags=["Notifications"])
async def get_my_notifications(user_id: Annotated[
                                            int,
                                            Depends(get_current_user_id)]):
    return users_controller.handle_get_notifications(user_id)


@app.delete("/users/me/notifications/{notification_id}",
            tags=["Notifications"])
async def delete_notification(user_id: Annotated[
                                            int,
                                            Depends(get_current_user_id)],
                              notification_id: int):
    return users_controller.handle_delete_notification(user_id,
                                                       notification_id)


@app.patch("/users/me/notifications/{notification_id}",
           tags=["Notifications"])
async def update_notification(user_id: Annotated[
                                            int,
                                            Depends(get_current_user_id)],
                              notification_id: int,
                              update_data: UpdateNotificationSchema):
    return users_controller.handle_update_notification(user_id,
                                                       notification_id,
                                                       update_data.dict())
