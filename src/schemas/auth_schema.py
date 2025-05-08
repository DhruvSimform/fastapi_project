from pydantic import BaseModel

class BaseToken(BaseModel):
    pass

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseToken):
    username: str
