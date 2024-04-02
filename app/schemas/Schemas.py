from pydantic import BaseModel
from typing import Dict
from datetime import date


class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    gender: str
    photo: str
    birthdate: date
    location: Dict


class CreateUserSchema(BaseModel):
    email: str


class LoginRequest(BaseModel):
    auth_code: str
