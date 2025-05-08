from pydantic import BaseModel


class BaseToken(BaseModel):
    pass


class Token(BaseToken):
    access_token: str
    refresh_token: str
    token_type: str


class RefreshToken(BaseToken):
    refresh_token: str


class TokenData(BaseToken):
    username: str
