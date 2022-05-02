from pydantic import BaseModel


class PostSchema(BaseModel):
    title: str = None
    text: str = None
    category_id: str = None


class CategorySchema(BaseModel):
    title: str | None = None


class TokenUserSchema(BaseModel):
    grant_type: str = None
    username: str | None = None
    password: str | None = None
    scopes: str = []
    client_id: str | None = None
    client_secret: str | None = None
