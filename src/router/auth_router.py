from typing import Annotated

from fastapi import APIRouter, Depends, Form, status
from sqlalchemy.orm import Session

from ..dependencies import get_current_user_and_db, get_db
from ..schemas.auth_schema import RefreshToken, Token
from ..schemas.user_schema import UserLogin, UserOutput
from ..service.auth_services import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

DB_Dependency = Annotated[Session, Depends(get_db)]
USER_DB_Dependency = Annotated[
    tuple[UserOutput, Session], Depends(get_current_user_and_db)
]


@router.post(
    "/token",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="User Login",
    description="""
    Authenticate a user and return an access token for accessing protected routes.
    This endpoint accepts a username and password via form data. If the credentials
    are valid, a JWT access token is returned, which can be used to authenticate
    future requests.

### Response Codes
- **200**: Token successfully generated.
- **401**: Invalid credentials.
""",
)
def login_user(data: Annotated[UserLogin, Form()], db: DB_Dependency):
    _service = AuthService(db)
    return _service.login_for_token(data)


@router.post(
    "/refresh-token",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Refresh Access Token",
    description="""
    Obtain a new access token using a valid refresh token.
    This endpoint is used to renew an expired or expiring access token by providing
    a valid refresh token.

### Response Codes
- **200**: New access token successfully generated.
- **401**: Invalid or expired refresh token.
""",
)
def refresh_access_token(token: RefreshToken):
    return AuthService.refresh_access_token(token.refresh_token)
