from typing import Annotated

from fastapi import APIRouter, Depends, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from ..dependencies import get_current_user_and_db, get_db
from ..schemas.auth_schema import Token
from ..schemas.user_schema import UserInput, UserOutput , UserRole
from ..service.users_services import UserServvice

router = APIRouter(prefix="/users", tags=["Users"])


DB_Depndancy = Annotated[Session, Depends(get_db)]

USER_DB_Dependancy = Annotated[
    tuple[UserOutput, Session], Depends(get_current_user_and_db)
]


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserOutput)
def create_user(data: UserInput, db: DB_Depndancy):
    _service = UserServvice(db)

    return _service.create(data)


@router.get("", response_model=list[UserOutput], status_code=status.HTTP_200_OK )
def get_users(user_db: USER_DB_Dependancy):
    user, db = user_db
    _service = UserServvice(db)
    return _service.get_all()


@router.get("/{id}", response_model=UserOutput, status_code=status.HTTP_200_OK)
def get_user(id: UUID4, user_db: USER_DB_Dependancy):
    _, db = user_db
    _service = UserServvice(db)
    return _service.get(id)

@router.delete("/{id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: UUID4, user_db: USER_DB_Dependancy):
    _ , db = user_db
    _service = UserServvice(db)
    return _service.delete(id)
