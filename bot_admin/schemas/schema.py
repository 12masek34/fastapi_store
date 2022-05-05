from pydantic import BaseModel


class PostSchema(BaseModel):
    title: str | None = None
    text: str | None = None
    category_id: str | None = None
    category_title: str | None = None


class CategorySchema(BaseModel):
    title: str | None = None


class TokenUserSchema(BaseModel):
    grant_type: str = None
    username: str | None = None
    password: str | None = None
    scopes: str = []
    client_id: str | None = None
    client_secret: str | None = None


class ImageSchema(BaseModel):
    post_id: int | None = None
    img: str | None = None
