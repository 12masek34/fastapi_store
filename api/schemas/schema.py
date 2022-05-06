from pydantic import BaseModel
from datetime import datetime


class AddPostSchema(BaseModel):
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


class CategoriesCountSchema(BaseModel):
    id: int
    title: str
    count: int

    class Config:
        orm_mode = True


class AddCategorySchema(BaseModel):
    title: str

    class Config:
        orm_mode = True


class OkSchema(BaseModel):
    status: str = 'ok'


class AddImageSchema(BaseModel):
    post_id: int
    img: str

    class Config:
        orm_mode = True


class ImageSchema(AddImageSchema):
    id: int


class PostSchema(BaseModel):
    id: int
    title: str
    text: str
    category_id: int
    created_at: datetime
    updated_at: datetime
    img: list[ImageSchema]

    class Config:
        orm_mode = True
