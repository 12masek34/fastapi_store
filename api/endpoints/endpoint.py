from models.database import session, Category, Post
from schemas.schema import CategorySchema, PostSchema, OkSchema
from schemas.auth_schema import TokenSchema
from fastapi.security import OAuth2PasswordRequestForm
from authorizations.authorization import Auth
from fastapi import Depends, HTTPException, status, APIRouter
from datetime import timedelta
from schemas.auth_schema import UserSchema

endpoints = APIRouter()
auth = Auth()

ok_response = {'status': 'ok'}


@endpoints.get('/categories', status_code=200, response_model=list[CategorySchema], tags=['categories'])
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


@endpoints.post("/token", response_model=TokenSchema)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    print(form_data.__dict__)
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


@endpoints.get("/users/me/", response_model=UserSchema)
async def read_users_me(current_user: UserSchema = Depends(auth.get_current_user)):
    return current_user
