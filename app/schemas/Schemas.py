from pydantic import BaseModel, HttpUrl
from typing import Optional


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


class UpdateUserSchema(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    photo: str
