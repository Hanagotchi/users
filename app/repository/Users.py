from sqlalchemy import create_engine, engine
from sqlalchemy.orm import Session
import os
from models.users import User


class UsersRepository:
    db_url = engine.URL.create(
        "postgresql",
        database=os.environ["POSTGRES_DB"],
        username=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host=os.environ["POSTGRES_HOST"],
        port=os.environ["POSTGRES_PORT"]
    )

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

    def get_user_by_name(self, name: str):
        user = self.session.query(User).filter_by(name=name).first()
        return user.__dict__ if user else None

    def get_all_users(self):
        users = self.session.query(User).all()
        return self.__parse_result(users)

    def create_user(self, name: str):
        new_user = User(name=name)
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def __parse_result(self, result):
        if not result:
            return []
        return [r.__dict__ for r in result]
