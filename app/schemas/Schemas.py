from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    name: str


class CreateUserSchema(BaseModel):
    name: str
    mail: str


class LoginRequest(BaseModel):
    auth_code: str
