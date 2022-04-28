from fastapi import APIRouter
from models.database import session, Category
from schemas.schema import CategorySchema

endpoints = APIRouter()


@endpoints.get('/categories', status_code=200, response_model=list[CategorySchema])
async def index():
    categories = session.query(Category).all()

    return categories
