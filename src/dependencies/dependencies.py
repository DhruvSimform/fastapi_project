from ..repository.user_repository import UserRepository
from fastapi import Depends  , HTTPException , status
from typing import Annotated
from ..utils.auth import verify_token
from fastapi.security import OAuth2PasswordBearer
from ..schemas.auth_schema import Token 
from ..schemas.user_schema import UserOutput
from ..config.database import get_db
from sqlalchemy.orm import Session
from ..service.user_services import UserServvice

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


def get_current_user_and_db(
    token: Annotated[Token, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)]
) -> tuple[UserOutput, Session]:
    print(token)
    payload = verify_token(token)
    username = payload.get("sub")

    user_service = UserServvice(db)
    user = user_service.repository.get_user_by_username(username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        ) 
    return user, db