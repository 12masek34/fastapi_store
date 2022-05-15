import os
from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

from models.database import get_db
from models.models import User
from schemas.auth_schema import UserSchemaInDB

load_dotenv()


class Auth:
    SECRET_KEY = os.getenv('SECRET_KEY')
    ALGORITHM = os.getenv('ALGORITHM')
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def __init__(self):
        self.pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
        self.session = next(get_db())
        self.db_user = User
        self.user: UserSchemaInDB | None = None
        self.encoded_jwt: str | None = None
        self.credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def authenticate_user(self, username: str, password: str):
        self.get_user(username)
        if not self.user:
            return False
        if not self.verify_password(password, self.user.hash_password):
            return False
        return self.user

    def get_user(self, username: str):
        user = self.session.query(self.db_user).filter(self.db_user.username == username).first()
        if user is None:
            pass
        else:
            self.user = UserSchemaInDB.from_orm(user)

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        self.encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return self.encoded_jwt

    async def check_auth(self, token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise self.credentials_exception
        except JWTError:
            raise self.credentials_exception
