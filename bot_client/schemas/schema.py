from pydantic import BaseModel


class TokenUserSchema(BaseModel):
    grant_type: str = None
    username: str | None = None
    password: str | None = None
    scopes: str = []
    client_id: str | None = None
    client_secret: str | None = None
