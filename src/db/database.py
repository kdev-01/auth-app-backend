from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from .config import get_settings
from .singleton import SingletonMeta

settings = get_settings()
DATABASE_URL = settings.DATABASE_URL
Base = declarative_base()


class Database(metaclass=SingletonMeta):
    def __init__(self):
        self.engine = create_engine(DATABASE_URL)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

    def get_session(self):
        return self.SessionLocal()
