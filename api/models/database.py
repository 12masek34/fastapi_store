import os
import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime, ForeignKey, Text, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()
engine = create_engine(os.getenv('DNS'))
meta = MetaData(bind=engine)
session = Session(bind=engine)


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer(), primary_key=True)
    title = Column(String(128), nullable=False)
    created_at = Column(DateTime(), default=datetime.datetime.now)
    posts = relationship('Post', cascade='all, delete-orphan')


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer(), primary_key=True)
    title = Column(String(128), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id', ondelete='CASCADE'), nullable=False)
    text = Column(Text(), nullable=False)
    created_at = Column(DateTime(), default=datetime.datetime.now)
    updated_at = Column(DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now)
    category = relationship('Category')
    img = relationship('Image', cascade='all, delete-orphan')


class Image(Base):
    __tablename__ = 'images'
    id = Column(Integer(), primary_key=True)
    post_id = Column(Integer, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    img = Column(String(200), nullable=False)
    post = relationship('Post')


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    username = Column(String(128), nullable=False)
    hash_password = Column(String(128), nullable=False)
    created_at = Column(DateTime(), default=datetime.datetime.now)

# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)
