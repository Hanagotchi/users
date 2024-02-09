
from fastapi import FastAPI
from controller.Users import UsersController
from service.Users import UsersService
from repository.Users import UsersRepository

app = FastAPI()
users_repository = UsersRepository()
users_service = UsersService(users_repository)
users_controller = UsersController(users_service)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/user/{user_id}")
async def get_users(user_id: int):
    print(f"holaaa, acaa desde el main {user_id}")
    return users_controller.handle_get_user(user_id)
