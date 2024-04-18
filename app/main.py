from fastapi import FastAPI
from controller.Users import UsersController
from service.Users import UsersService
from repository.Users import UsersRepository
from schemas.Schemas import CreateUserSchema, UpdateUserSchema
from schemas.Schemas import LoginRequest
from typing import List, Annotated, Union
from fastapi import FastAPI, Query

app = FastAPI()
users_repository = UsersRepository()
users_service = UsersService(users_repository)
users_controller = UsersController(users_service)


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/users/{user_id}")
def get_users(user_id: int):
    return users_controller.handle_get_user(user_id)


@app.get("/users")
def get_all_users(ids: Annotated[Union[List[str], None], Query()] = None):
    if ids:
        ids = ids[0].split(",")
        return users_controller.handle_get_all_users(ids)
    else:
        return users_controller.handle_get_all_users()


@app.post("/users")
async def create_user(user_data: CreateUserSchema):
    return await users_controller.handle_create_user(user_data.dict())


@app.post("/login")
async def login_with_google(request: LoginRequest):
    return await users_controller.handle_login(request.auth_code)


@app.patch("/users/{user_id}")
def update_user(user_id: int, update_data: UpdateUserSchema):
    return users_controller.handle_update_user(user_id, update_data.dict())
