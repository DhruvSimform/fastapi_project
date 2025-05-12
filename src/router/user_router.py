from typing import Annotated

from fastapi import APIRouter, Depends, status , Body
from pydantic import UUID4
from sqlalchemy.orm import Session

from ..dependencies import get_admin_user_and_db, get_current_user_and_db, get_db
from ..schemas.auth_schema import Token
from ..schemas.user_schema import UpdateUser, UserInput, UserOutput, UserDetailedOutput
from ..service.users_services import UserService

router = APIRouter(prefix="/users", tags=["Users"])


DB_Depndancy = Annotated[Session, Depends(get_db)]

USER_DB_Dependancy = Annotated[
    tuple[UserDetailedOutput, Session], Depends(get_current_user_and_db)
]

ADMIN_USER_DB_Dependancy = Annotated[
    tuple[UserDetailedOutput, Session], Depends(get_admin_user_and_db)
]


from fastapi import Body
from typing import Annotated
from fastapi.responses import JSONResponse

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=UserDetailedOutput,
)
def create_user(data: Annotated[UserInput,
    Body(
        title="User Input",
        description="Payload to create a new user account.",
    )],
    db: DB_Depndancy):

    _service = UserService(db)
    return _service.create(data)



@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[UserOutput | UserDetailedOutput],
)
def get_users(user_db: USER_DB_Dependancy):
    user, db = user_db
    _service = UserService(db)
    return _service.get_all(user.role)

@router.patch("/me", status_code=status.HTTP_200_OK , response_model=UserDetailedOutput)
def update_user(data: UpdateUser, user_db: USER_DB_Dependancy):
    user, db = user_db
    _service = UserService(db)
    return _service.update_user(user.username, data=data)

@router.get("/me", status_code=status.HTTP_200_OK , response_model=UserDetailedOutput)
def get_profile_details(user_db: USER_DB_Dependancy):
    user, db = user_db
    _service = UserService(db)
    print(user.id)
    return _service.get(user.id)



@router.get("/profile/{username}", response_model=UserDetailedOutput | UserOutput, status_code=status.HTTP_200_OK)
def get_user_username(username: str, user_db: USER_DB_Dependancy):
    user, db = user_db
    _service = UserService(db)
    return _service.get_by_username(user.role,username)

@router.get("/{id}", response_model=UserDetailedOutput, status_code=status.HTTP_200_OK , deprecated=True)
def get_user_by_id(id: UUID4, user_db: USER_DB_Dependancy):
    _, db = user_db
    _service = UserService(db)
    return _service.get(id)

@router.delete("/{id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: UUID4, user_db: ADMIN_USER_DB_Dependancy):
    _, db = user_db
    _service = UserService(db)
    return _service.delete_user(id)


