from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base=declarative_base()

class DBConnection:
    def __init__(self):
        self.__engine = None
        self.__connect_url = "sqlite:///database.db"
        self.session = None
    def connect_to_db(self):
        self.__engine= create_engine(self.__connect_url)
    
    def get_engine(self):
        return self.__engine

    def __enter__(self):
        Session = sessionmaker()
        self.session = Session(bind=self.__engine)
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()

db_connection = DBConnection()