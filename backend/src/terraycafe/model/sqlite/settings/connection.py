from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from typing import Generator


Base = declarative_base()

DATABASE_URL = "sqlite:///database.db"


engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

class DBConnection:
    def __init__(self):
        self.__engine = engine
        self.session = None

    def get_engine(self):
        return self.__engine

    def __enter__(self):
        self.session = SessionLocal()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.close()

db_connection = DBConnection()

def get_db() -> Generator[Session, None, None]:
    with db_connection as db:
        yield db
