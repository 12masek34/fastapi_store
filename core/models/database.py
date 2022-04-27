import datetime

from sqlalchemy import create_engine, Column, String, Integer, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

engine = create_engine('postgresql+psycopg2://postgres:123@localhost/postgres')


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Numeric(), primary_key=True)
    title = Column(String(128), nullable=False)
    category = Column(String(128), nullable=False)
    text = Column(Text(), nullable=False)
    created_at = Column(DateTime(), default=datetime.datetime.now)
    updated_at = Column(DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now)


Base.metadata.create_all(engine)
