from sqlalchemy import Column, Integer, String
from models.database import Base
from os import environ


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": environ.get(
        "POSTGRES_SCHEMA",
        "users_service")}
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=False)
    gender = Column(String, nullable=True)
    photo = Column(String, nullable=True)
