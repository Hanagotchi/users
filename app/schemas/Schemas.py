from datetime import date
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict
from datetime import datetime


class UserSchema(BaseModel):
    id: int
    name: str
    email: str
    gender: str
    photo: str
    birthdate: date
    location: Dict
    nickname: str
    biography: str
    device_token: str


class CreateUserSchema(BaseModel):
    email: str
    name: Optional[str] = None
    gender: Optional[str] = None
    photo: Optional[str] = None
    birthdate: Optional[date] = None
    location: Optional[Dict] = None
    nickname: Optional[str] = None
    biography: Optional[str] = None


class LoginRequest(BaseModel):
    auth_code: str


class UpdateUserSchema(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    photo: Optional[str] = None
    birthdate: Optional[date] = None
    location: Optional[Dict] = None
    nickname: Optional[str] = None
    biography: Optional[str] = None
    device_token: Optional[str] = None


class CreateNotificationSchema(BaseModel):
    date_time: datetime = Field(..., alias='date_time')
    content: str = Field(..., max_length=128)

    @validator('date_time')
    def validate_date_time(cls, v):
        if v.minute % 5 != 0:
            raise ValueError('Minutes must be multiples of 5')
        return v


class UpdateNotificationSchema(BaseModel):
    date_time: Optional[datetime] = Field(..., alias='date_time')
    content: Optional[str] = Field(..., max_length=128)

    @validator('date_time')
    def validate_date_time(cls, v):
        if v.minute % 5 != 0:
            raise ValueError('Minutes must be multiples of 5')
        return v
