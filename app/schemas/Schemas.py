from datetime import date
from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict


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
    name: Optional[str] = None
    gender: Optional[str] = None
    photo: Optional[str] = None
    birthdate: Optional[date] = None
    location: Optional[Dict] = None


class LoginRequest(BaseModel):
    auth_code: str


class UpdateUserSchema(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    photo: Optional[HttpUrl] = None
