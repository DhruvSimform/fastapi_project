from .auth import get_current_user_and_db
from typing import Annotated
from ..schemas.user_schema import UserOutput , UserRole
from fastapi import Depends , HTTPException , status
from sqlalchemy.orm import Session

USER_DB_Dependancy = Annotated[
    tuple[UserOutput, Session], Depends(get_current_user_and_db)
]


def get_admin_user_and_db(user_db: USER_DB_Dependancy) -> tuple[UserOutput, Session]:

    user, db = user_db

    if user.role != UserRole.admin:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only Admin User Can Delete Account of User"
        )

    return user, db
