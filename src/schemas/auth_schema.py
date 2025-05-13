from typing import Optional

from pydantic import BaseModel, Field


class BaseToken(BaseModel):
    pass


class Token(BaseToken):
    access_token: str = Field(..., description="Access token for authentication")
    refresh_token: str = Field(
        ..., description="Refresh token for obtaining a new access token"
    )
    token_type: str = Field(..., description="Type of the token, typically 'Bearer'")


class RefreshToken(BaseToken):
    refresh_token: str = Field(
        ..., description="Refresh token for obtaining a new access token"
    )


class TokenData(BaseToken):
    username: Optional[str] = Field(
        None, description="Username associated with the token"
    )
