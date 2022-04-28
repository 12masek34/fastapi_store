from pydantic import BaseModel


class Post(BaseModel):
    title: str = None
    text: str = None
    category: str = None


