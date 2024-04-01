from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from os import environ
from typing import Optional
from models.database import Base
from models.users import User


class UsersRepository:
    db_url = environ.get(
                    "DATABASE_URL").replace(
                        "postgres://",
                        "postgresql://",
                        1)

    engine = create_engine(db_url)

    def __init__(self):
        self.conn = self.engine.connect()
        self.session = Session(self.engine)

    def shutdown(self):
        self.conn.close()
        self.session.close()

    def rollback(self):
        self.session.rollback()

    def add(self, record: Base):
        self.session.add(record)
        self.session.commit()

    def get_user(self, user_id: int):
        user = self.session.query(User).filter_by(id=user_id).first()
        return user.__dict__ if user else None

    def get_user_by_email(self, email: str):
        user = self.session.query(User).filter_by(email=email).first()
        return user.__dict__ if user else None

    def get_all_users(self):
        users = self.session.query(User).all()
        return self.__parse_result(users)

    def create_user(
        self,
        email: str,
        name: Optional[str] = None,
        gender: Optional[str] = None,
        photo: Optional[str] = None,
    ) -> User:
        user_data = {"email": email}

        if name is not None:
            user_data["name"] = name
        if gender is not None:
            user_data["gender"] = gender
        if photo is not None:
            user_data["photo"] = photo

        new_user = User(**user_data)
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def edit_user(self, user_id: int, data_to_edit: dict):
        user = self.session.query(User).filter_by(id=user_id).first()
        for field, value in data_to_edit.items():
            setattr(user, field, value)

        self.session.commit()
        return user

    def __parse_result(self, result):
        if not result:
            return []
        return [r.__dict__ for r in result]
