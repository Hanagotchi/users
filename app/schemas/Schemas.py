from pydantic import BaseModel
from typing import Dict

class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    gender: str
    photo: str
    location: Dict


class CreateUserSchema(BaseModel):
    email: str


class LoginRequest(BaseModel):
    auth_code: str
