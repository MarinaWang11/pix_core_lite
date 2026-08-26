# Connection of the application to the SQLite
# FastApi -> database.py -> pix_core.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = "sqlite:///./pix_core.db" 

#Engine is the conection to the database
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}) #False only for SQLite

#Sessions are used to interact with the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal() #open a new session 

    try:
        yield db #deliver it
        
    finally:
        db.close() #close it


class Base(DeclarativeBase):
    pass