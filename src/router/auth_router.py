from fastapi import APIRouter , Depends , status , Form
from pydantic import UUID4
from sqlalchemy.orm import Session
from ..schemas.user_schema import UserInput,UserOutput , UserLogin
from ..schemas.auth_schema import Token , RefreshToken
from ..service.user_services import UserServvice
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from ..dependencies import get_db , get_current_user_and_db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


DB_Depndancy = Annotated[Session , Depends(get_db)]

USER_DB_Dependancy = Annotated[tuple[UserOutput, Session], Depends(get_current_user_and_db)]


@router.post("/token" , response_model=Token , status_code=status.HTTP_200_OK)
def login_user(data: Annotated[UserLogin , Form()] , db: DB_Depndancy):
    _service = UserServvice(db)
    return _service.login_for_token(data)


@router.post("/refresh-token" , response_model=Token , status_code=status.HTTP_200_OK)
def refresh_access_token(token:RefreshToken):
    return UserServvice.genrate_new_access_token(token.refresh_token)

    