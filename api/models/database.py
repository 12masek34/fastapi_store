import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_URL_DATABASE = os.getenv('URL_DB')
TEST_SQLALCHEMY_URL_DATABASE = os.getenv('URL_TEST_DB')

Base = declarative_base()
engine = create_engine(SQLALCHEMY_URL_DATABASE)
meta = MetaData(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_db() -> None:
    """
    Проверяет, если нет БД, то создает БД и таблицы.
    """
    if not database_exists(engine.url):
        create_database(engine.url)
    Base.metadata.create_all(engine)


def drop_db() -> None:
    """
    Только для разработки.
    """
    Base.metadata.drop_all(engine)
