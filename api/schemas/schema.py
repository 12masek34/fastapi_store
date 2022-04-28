from pydantic import BaseModel
from datetime import datetime


class Post(BaseModel):
    title: str
    category: str
    text: str


class CategorySchema(BaseModel):
    id: int
    title: str
    created_at: datetime

    class Config:
        orm_mode = True


