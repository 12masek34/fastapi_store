from fastapi import APIRouter
from models.database import session, Category

endpoints = APIRouter()


@endpoints.get('/categories', status_code=200)
async def index():
    resp = session.query(Category).all()
    return resp
