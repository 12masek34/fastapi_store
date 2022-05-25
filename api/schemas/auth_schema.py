import datetime

from pydantic import BaseModel


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenDataSchema(BaseModel):
    username: str | None = None


class UserSchema(BaseModel):
    id: int
    username: str
    created_at: datetime.datetime


class UserSchemaInDB(UserSchema):
    hash_password: str

    class Config:
        orm_mode = True


class RegistrationSchema(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
