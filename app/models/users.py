from sqlalchemy import Column, Integer, String
from models.database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = {'schema': 'dev'}
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=True)
    email = Column(String, nullable=False)
    gender = Column(String, nullable=True)
    photo = Column(String, nullable=True)
