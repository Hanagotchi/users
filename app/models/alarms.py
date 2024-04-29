from sqlalchemy import ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from models.database import Base
from os import environ


SCHEMA = environ.get("POSTGRES_SCHEMA", "users_service")


class Alarm(Base):
    __tablename__ = "alarms"
    __table_args__ = {"schema": SCHEMA}

    id: Mapped[int] = mapped_column(Integer,
                                    primary_key=True,
                                    autoincrement=True)
    id_user: Mapped[int] = mapped_column(ForeignKey(f"{SCHEMA}.users.id"),
                                         nullable=False, unique=True)
    datetime: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, nullable=False)
    content: Mapped[str] = mapped_column(String(128), nullable=False)

    def __repr__(self) -> str:
        return (
            f"Alarm(id={self.id}, "
            f"id_user={self.id_user}, "
            f"datetime={self.datetime}, "
            f"content={self.content})"
        )
