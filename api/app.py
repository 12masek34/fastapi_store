from datetime import timedelta

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from schemas.schema import (CategorySchema, AddPostSchema, AddCategorySchema, PostSchema, AddImageSchema,
                            CategoriesCountSchema, ImageSchema)
from schemas.auth_schema import TokenSchema
from authorizations.authorization import Auth
from models.database import get_db
from models import crud

endpoints = APIRouter()
auth = Auth()


@endpoints.get('/categories', status_code=200, response_model=list[CategorySchema], tags=['categories'],
               dependencies=[(Depends(auth.check_auth))])
async def categories_all(db: Session = Depends(get_db)):
    categories = crud.get_all_category(db)
    if len(categories) == 0:
        raise HTTPException(status_code=404, detail='Category not found')
    return categories


@endpoints.get('/categories/count', status_code=200, response_model=list[CategoriesCountSchema], tags=['categories'],
               dependencies=[(Depends(auth.check_auth))])
async def categories_all_count(db: Session = Depends(get_db)):
    categories = crud.get_all_count_category(db)
    if categories:
        return categories
    raise HTTPException(status_code=404, detail='Categories not found')


@endpoints.delete('/categories/{category_id}', status_code=200, response_model=CategorySchema,
                  tags=['categories'],
                  dependencies=[(Depends(auth.check_auth))])
async def categories_delete(category_id: int, db: Session = Depends(get_db)):
    return crud.delete_category(db, category_id)


@endpoints.get('/categories/{category_id}', status_code=200, response_model=CategorySchema, tags=['categories'],
               dependencies=[(Depends(auth.check_auth))])
async def category_filter(category_id: int, db: Session = Depends(get_db)):
    category = crud.get_category_by_id(db, category_id)
    if category:
        return category
    raise HTTPException(status_code=404, detail='Category not found')


@endpoints.post('/category/add', status_code=201, response_model=CategorySchema, tags=['categories'],
                dependencies=[(Depends(auth.check_auth))])
async def category_create(data: AddCategorySchema, db: Session = Depends(get_db)):
    return crud.create_category(db, data)


@endpoints.get('/posts/category/{category_id}', status_code=200, response_model=list[PostSchema], tags=['posts'],
               dependencies=[(Depends(auth.check_auth))])
async def posts_filter_by_category(category_id: int, db: Session = Depends(get_db)):
    posts = crud.get_posts_by_category_id(db, category_id)
    if posts:
        return posts
    raise HTTPException(status_code=404, detail='Posts not found')


@endpoints.post('/post/add', status_code=201, response_model=PostSchema, tags=['posts'],
                dependencies=[(Depends(auth.check_auth))])
async def post_add(data: AddPostSchema, db: Session = Depends(get_db)):
    return crud.create_post(db, data)


@endpoints.get('/posts', status_code=200, response_model=list[PostSchema], tags=['posts'],
               dependencies=[(Depends(auth.check_auth))])
async def posts_all(db: Session = Depends(get_db)):
    return crud.get_all_posts(db)


@endpoints.post('/images/add', status_code=201, response_model=ImageSchema, tags=['images'],
                dependencies=[(Depends(auth.check_auth))])
async def image_add(data: AddImageSchema, db: Session = Depends(get_db)):
    return crud.update_post_add_image(db, data)


@endpoints.post("/token", status_code=200, response_model=TokenSchema, tags=['token'])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
