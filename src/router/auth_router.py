from typing import Annotated

from fastapi import APIRouter, Depends, Form, status
from sqlalchemy.orm import Session

from ..dependencies import get_current_user_and_db, get_db
from ..schemas.auth_schema import RefreshToken, Token
from ..schemas.user_schema import UserInput, UserLogin, UserOutput
from ..service.auth_services import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


DB_Depndancy = Annotated[Session, Depends(get_db)]

USER_DB_Dependancy = Annotated[
    tuple[UserOutput, Session], Depends(get_current_user_and_db)
]


@router.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
def login_user(data: Annotated[UserLogin, Form()], db: DB_Depndancy):
    _service = AuthService(db)
    return _service.login_for_token(data)


@router.post("/refresh-token", response_model=Token, status_code=status.HTTP_200_OK)
def refresh_access_token(token: RefreshToken):
    return AuthService.refresh_access_token(token.refresh_token)
