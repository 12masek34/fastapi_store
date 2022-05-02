from pydantic import BaseModel
from datetime import datetime


class PostSchema(BaseModel):
    title: str
    category_id: int
    text: str

    class Config:
        orm_mode = True


class CategorySchema(BaseModel):
    id: int
    title: str
    created_at: datetime

    class Config:
        orm_mode = True


class AddCategorySchema(BaseModel):
    title: str

    class Config:
        orm_mode = True


class OkSchema(BaseModel):
    status: str = 'ok'
