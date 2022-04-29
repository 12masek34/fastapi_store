from fastapi import APIRouter
from models.database import session, Category, Post
from schemas.schema import CategorySchema, PostSchema, OkSchema

endpoints = APIRouter()

ok_response = {'status': 'ok'}


@endpoints.get('/categories', status_code=200, response_model=list[CategorySchema])
async def all_categories():
    categories = session.query(Category).all()

    return categories


@endpoints.post('/add/post', status_code=201, response_model=OkSchema)
async def add_post(data: PostSchema):
    post = Post(
        title=data.title,
        category_id=data.category_id,
        text=data.text
    )
    session.add(post)
    session.commit()
    return ok_response
