from pydantic import BaseModel
from datetime import datetime


class Post(BaseModel):
    title: str
    category: str
    text: str


class Category(BaseModel):
    id: int
    title: str
    created_at: datetime


class Categories(BaseModel):
    category: list[Category]
