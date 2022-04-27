from fastapi import APIRouter

endpoints = APIRouter()


@endpoints.get('/')
async def index():
    return {'a': 'b'}
