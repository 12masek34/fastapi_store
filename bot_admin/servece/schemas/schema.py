from pydantic import BaseModel


class PostSchema(BaseModel):
    title: str = None
    text: str = None
    category: str = None


