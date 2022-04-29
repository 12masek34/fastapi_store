from pydantic import BaseModel


class PostSchema(BaseModel):
    title: str = None
    text: str = None
    category_id: str = None

