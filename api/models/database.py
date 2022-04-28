import datetime

from sqlalchemy import create_engine, Column, String, Integer, DateTime, ForeignKey, Numeric, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, Session

Base = declarative_base()

engine = create_engine('postgresql+psycopg2://postgres:123@localhost/postgres')

session = Session(bind=engine)


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer(), primary_key=True)
    title = Column(String(128), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    text = Column(Text(), nullable=False)
    created_at = Column(DateTime(), default=datetime.datetime.now)
    updated_at = Column(DateTime(), default=datetime.datetime.now, onupdate=datetime.datetime.now)
    category = relationship('Category', backref='posts')


class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer(), primary_key=True)
    title = Column(String(128), nullable=False)
    created_at = Column(DateTime(), default=datetime.datetime.now)


# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)
a = session.query(Category).all()


# p = Post(
#     title='title',
#     # category_id=1,
#     text='text',
#     category=a
# )
# a1 = Category(title='Транспорт')
# a2 = Category(title='Недвижимость')
# a3 = Category(title='Техника')
# a4 = Category(title='Запчасти')
# a5 = Category(title='Работа')
# session.add_all([a1, a2, a3, a4, a5])
# session.commit()
