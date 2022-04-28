from pydantic import BaseModel


class Post(BaseModel):
    title: str = None
    category: str = None
    text: str = None
