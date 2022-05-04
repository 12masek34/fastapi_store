import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime, ForeignKey, Text, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session, backref

# from migrate.versioning.schema import Table, Column


Base = declarative_base()

engine = create_engine('postgresql+psycopg2://postgres:123@localhost/postgres')
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


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer(), primary_key=True)
    username = Column(String(128), nullable=False)
    hash_password = Column(String(128), nullable=False)
    created_at = Column(DateTime(), default=datetime.datetime.now)


# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)

#
# table = Table('users', meta)
# col = Column('name', String(128), nullable=False)
# col.create(table)
# table.drop()

#
# a = User(
#     username='Dmitriy_Martys',
#     hash_password='$2b$12$kyf7o75xzLg0R77GvSHdw.RFsVHn7OmbDxjZVNX4kgs35pBt5/9AO'
# )
# session.add(a)
# session.commit()
