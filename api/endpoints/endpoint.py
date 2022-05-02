from models.database import session, Category, Post
from schemas.schema import CategorySchema, PostSchema, OkSchema, AddCategorySchema
from schemas.auth_schema import TokenSchema
from fastapi.security import OAuth2PasswordRequestForm
from authorizations.authorization import Auth
from fastapi import Depends, HTTPException, status, APIRouter
from datetime import timedelta

endpoints = APIRouter()
auth = Auth()

ok_response = {'status': 'ok'}


@endpoints.get('/categories', status_code=200, response_model=list[CategorySchema], tags=['categories'],
               dependencies=[(Depends(auth.check_auth))])
async def all_categories():
    categories = session.query(Category).all()

    return categories


@endpoints.post('/add/post', status_code=201, response_model=OkSchema, tags=['posts'],
                dependencies=[(Depends(auth.check_auth))])
async def add_post(data: PostSchema):
    post = Post(
        title=data.title,
        category_id=data.category_id,
        text=data.text
    )
    session.add(post)
    session.commit()

    return ok_response


@endpoints.post('/add/category', status_code=201, response_model=OkSchema, tags=['categories'],
                dependencies=[(Depends(auth.check_auth))])
async def add_category(data: AddCategorySchema):
    category = Category(title=data.title)
    session.add(category)
    session.commit()

    return ok_response


@endpoints.post("/token", response_model=TokenSchema)
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
