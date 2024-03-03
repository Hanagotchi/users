from sqlalchemy import create_engine, engine
from sqlalchemy.orm import Session
from os import environ
from typing import Optional
from models.users import User


class UsersRepository:
    db_url = environ.get("DATABASE_URL", engine.URL.create(
        "postgres",
        database=environ.get("POSTGRES_DB", "dev"),
        username=environ.get("POSTGRES_USER", "user"),
        password=environ.get("POSTGRES_PASSWORD", "1234"),
        host=environ.get("POSTGRES_HOST", "sql"),
        port=environ.get("POSTGRES_PORT", "5432")
    )).replace("postgres://", "postgresql://", 1)

    engine = create_engine(db_url)

    def __init__(self):
        self.conn = self.engine.connect()
        self.session = Session(self.engine)

    def shutdown(self):
        self.conn.close()
        self.session.close()

    def rollback(self):
        self.session.rollback()

    def get_user(self, user_id: int):
        user = self.session.query(User).filter_by(id=user_id).first()
        return user.__dict__ if user else None

    def get_user_by_email(self, email: str):
        user = self.session.query(User).filter_by(email=email).first()
        return user.__dict__ if user else None

    def get_all_users(self):
        users = self.session.query(User).all()
        return self.__parse_result(users)

    def create_user(self, email: str,
                    name: Optional[str] = None,
                    gender: Optional[str] = None,
                    photo: Optional[str] = None):
        user_data = {'email': email}

        if name is not None:
            user_data['name'] = name
        if gender is not None:
            user_data['gender'] = gender
        if photo is not None:
            user_data['photo'] = photo

        new_user = User(**user_data)
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def __parse_result(self, result):
        if not result:
            return []
        return [r.__dict__ for r in result]
