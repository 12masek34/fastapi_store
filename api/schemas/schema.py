from pydantic import BaseModel
from datetime import datetime


class PostSchema(BaseModel):
    title: str
    category_id: int
    text: str


class CategorySchema(BaseModel):
    id: int
    title: str
    created_at: datetime

    class Config:
        orm_mode = True


class OkSchema(BaseModel):
    status: str = 'ok'
