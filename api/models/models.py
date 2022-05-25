import datetime

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship

from models.database import Base


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer(), primary_key=True)
    title = Column(String(128), nullable=False)
    created_at = Column(DateTime(), default=datetime.datetime.now)

    posts = relationship('Post', backref='category', cascade='all, delete-orphan')

    def __repr__(self):
        return f'{self.__class__.__name__}({self.id!r},{self.title!r},{self.created_at!r})'

class Post(Base):
    __tablename__ = 'post'

    id = Column(Integer(), primary_key=True)
    title = Column(String(128), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    text = Column(Text(), nullable=False)
    created_at = Column(DateTime(), default=datetime.datetime.now)
    updated_at = Column(DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now)
    img = relationship('Image', backref='post', cascade='all, delete-orphan')

    def __repr__(self):
        return f'{self.__class__.__name__}'


class Image(Base):
    __tablename__ = 'image'

    id = Column(Integer(), primary_key=True)
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
    img = Column(String(200), nullable=False)

    def __repr__(self):
        return f'{self.__class__.__name__}'


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True)
    username = Column(String(128), nullable=False, unique=True)
    hash_password = Column(String(128), nullable=False)
    created_at = Column(DateTime(), default=datetime.datetime.now)

    def __repr__(self):
        return f'{self.__class__.__name__}'

