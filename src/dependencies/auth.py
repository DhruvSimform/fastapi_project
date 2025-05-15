from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ..config.database import get_db
from ..schemas.auth_schema import Token
from ..schemas.user_schema import UserDetailedOutput
from ..service.users_services import UserService
from ..utils.auth import verify_token

from sqlalchemy.ext.asyncio import AsyncSession

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_user_and_db(
    token: Annotated[Token, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)],
) -> tuple[UserDetailedOutput, AsyncSession]:

    payload = verify_token(token)
    username = payload.get("sub")

    user_service = UserService(db)
    user = await user_service.repository.get_user_all_detail_by_username(username)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user, db
