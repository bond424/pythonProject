from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from utils.config.config import db_postgre

DATABASE_URL = db_postgre.get('db-url')
DATABASE_USER = db_postgre.get('user')
DATABASE_PASSWORD = db_postgre.get('password')

DATABASE_HOST, DATABASE_NAME = DATABASE_URL.split('/')
SQLALCHEMY_DATABASE_URL = f'postgresql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db_session: Session = sessionLocal()
    try:
        yield db_session
    finally:
        db_session.close()
