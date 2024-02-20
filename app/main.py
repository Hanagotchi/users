from fastapi import FastAPI
from fastapi import Body
from controller.Users import UsersController
from service.Users import UsersService
from repository.Users import UsersRepository
from schemas.Schemas import CreateUserSchema
from schemas.Schemas import LoginRequest


app = FastAPI()
users_repository = UsersRepository()
users_service = UsersService(users_repository)
users_controller = UsersController(users_service)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users/{user_id}")
async def get_users(user_id: int):
    return users_controller.handle_get_user(user_id)


@app.get("/users")
async def get_all_users():
    return users_controller.handle_get_all_users()


@app.post("/users")
async def create_user(user_data: CreateUserSchema):
    return users_controller.handle_create_user(user_data.dict())


@app.post("/login")
def login_with_google(request: LoginRequest):
    return users_controller.handle_login(request.auth_code)
