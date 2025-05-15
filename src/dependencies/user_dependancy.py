from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..config.constant import UserRole
from ..schemas.user_schema import UserDetailedOutput
from .auth import get_current_user_and_db

USER_DB_Dependancy = Annotated[
    tuple[UserDetailedOutput, Session], Depends(get_current_user_and_db)
]

from sqlalchemy.ext.asyncio import AsyncSession

async def get_admin_user_and_db(
    user_db: USER_DB_Dependancy,
) -> tuple[UserDetailedOutput, AsyncSession]:

    user, db = user_db

    if user.role != UserRole.admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action.",
        )

    return user, db
