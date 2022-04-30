from models.database import session, User
from schemas.auth_schema import UserSchemaInDB, TokenDataSchema
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext


class Auth:
    SECRET_KEY = "90af17216c989ca797231e70a7d88011406cf31607bcbc21be29ea4114701c7c"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def __init__(self):
        self.pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
        self.session = session
        self.db_user = User
        self.user: UserSchemaInDB | None = None
        self.encoded_jwt: str | None = None

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

    async def get_current_user(self, token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenDataSchema(username=username)
        except JWTError:
            raise credentials_exception
        self.get_user(username=token_data.username)
        if self.user is None:
            raise credentials_exception
        return self.user

    async def check_auth(self, token: str = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            token_data = TokenDataSchema(username=username)
        except JWTError:
            raise credentials_exception
