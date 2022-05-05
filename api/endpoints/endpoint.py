from sqlalchemy import func

from models.database import session, Category, Post, Image
from schemas.schema import (CategorySchema, AddPostSchema, OkSchema, AddCategorySchema, PostSchema, AddImageSchema,
                            CategoriesCountSchema)
from schemas.auth_schema import TokenSchema
from fastapi.security import OAuth2PasswordRequestForm
from authorizations.authorization import Auth
from fastapi import Depends, HTTPException, status, APIRouter
from pydantic.error_wrappers import ValidationError

from datetime import timedelta

endpoints = APIRouter()
auth = Auth()

ok_response = {'status': 'ok'}


@endpoints.get('/categories', status_code=200, response_model=list[CategorySchema], tags=['categories'],
               dependencies=[(Depends(auth.check_auth))])
async def categories_all():
    categories = session.query(Category).all()

    return categories


@endpoints.get('/categories/count', status_code=200, response_model=list[CategoriesCountSchema], tags=['categories'],
               dependencies=[(Depends(auth.check_auth))])
async def categories_all_count():
    categories = session.query(Category.id, Category.title).order_by(Category.id).all()
    counts = session.query(func.count(Post.id)).group_by(Post.category_id).order_by(Post.category_id).all()
    list_resp = []
    for cat, count in zip(categories, counts):
        resp = dict()
        resp['id'] = cat[0]
        resp['title'] = cat[1]
        resp['count'] = count[0]
        list_resp.append(resp)


    return list_resp


@endpoints.delete('/categories/{category_id}', status_code=200, response_model=CategorySchema,
                  tags=['categories'],
                  dependencies=[(Depends(auth.check_auth))])
async def categories_delete(category_id: int):
    filter_category = session.query(Category).filter(Category.id == category_id).one()
    if category:
        session.delete(filter_category)
        session.commit()
        return filter_category
    else:
        raise HTTPException(status_code=404, detail='Category not found')


@endpoints.get('/categories/{category_id}', status_code=200, response_model=CategorySchema, tags=['categories'],
               dependencies=[(Depends(auth.check_auth))])
async def category(category_id: int):
    filter_category = session.query(Category).filter(Category.id == category_id).one()
    if filter_category:
        return filter_category
    else:
        raise HTTPException(status_code=404, detail='Category not found')


@endpoints.post('/category/add', status_code=201, response_model=OkSchema, tags=['categories'],
                dependencies=[(Depends(auth.check_auth))])
async def category_add(data: AddCategorySchema):
    category = Category(title=data.title)
    session.add(category)
    session.commit()

    return ok_response


@endpoints.get('/posts/{post_id}', status_code=200, response_model=list[PostSchema], tags=['posts'],
               dependencies=[(Depends(auth.check_auth))])
async def post(post_id: int):
    filter_posts = session.query(Post).filter(Post.category_id == post_id).all()
    if filter_posts:
        return filter_posts
    else:
        raise HTTPException(status_code=404, detail='Posts not found')


@endpoints.post('/post/add', status_code=201, response_model=int, tags=['posts'],
                dependencies=[(Depends(auth.check_auth))])
async def post_add(data: AddPostSchema):
    post = Post(
        title=data.title,
        category_id=data.category_id,
        text=data.text
    )
    session.add(post)
    session.flush()
    session.commit()

    return post.id


@endpoints.get('/posts', status_code=200, response_model=list[PostSchema], tags=['posts'],
               dependencies=[(Depends(auth.check_auth))])
async def categories_all():
    post = session.query(Post).all()

    return post


@endpoints.post('/images/add', status_code=200, response_model=OkSchema, tags=['images'],
                dependencies=[(Depends(auth.check_auth))])
async def image_add(data: AddImageSchema):
    img = Image(
        post_id=data.post_id,
        img=data.img
    )
    session.add(img)
    session.commit()


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
