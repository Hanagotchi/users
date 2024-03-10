from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    gender: str
    photo: str


class CreateUserSchema(BaseModel):
    email: str


class LoginRequest(BaseModel):
    auth_code: str
