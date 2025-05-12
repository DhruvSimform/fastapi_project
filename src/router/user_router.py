from typing import Annotated

from fastapi import APIRouter, Depends, status , Body
from pydantic import UUID4
from sqlalchemy.orm import Session

from ..dependencies import get_admin_user_and_db, get_current_user_and_db, get_db
from ..schemas.auth_schema import Token
from ..schemas.user_schema import UpdateUser, UserInput, UserOutput, UserOutputAdmin
from ..service.users_services import UserServvice

router = APIRouter(prefix="/users", tags=["Users"])


DB_Depndancy = Annotated[Session, Depends(get_db)]

USER_DB_Dependancy = Annotated[
    tuple[UserOutput, Session], Depends(get_current_user_and_db)
]

ADMIN_USER_DB_Dependancy = Annotated[
    tuple[UserOutput, Session], Depends(get_admin_user_and_db)
]


from fastapi import Body
from typing import Annotated
from fastapi.responses import JSONResponse

@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=UserOutput,
    summary="Create a new user",
    description=(
        "Registers a new user in the system.\n\n"
        "Clients should provide unique username, valid email, and a strong password. "
        "The response includes the newly created user's ID, username, email, and role. "
        "Note: Default role is 'user' unless specified otherwise by the admin."
    ),
    response_description="Returns the created user's data",
)
def create_user(
  data: Annotated[
    UserInput,
    Body(
        title="User Input",
        description="Payload to create a new user account.",
    )
],
    db: DB_Depndancy
):

    _service = UserServvice(db)
    return _service.create(data)



@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[UserOutput | UserOutputAdmin],
)
def get_users(user_db: USER_DB_Dependancy):
    user, db = user_db
    _service = UserServvice(db)
    return _service.get_all(user.role)


@router.get("/{id}", response_model=UserOutput, status_code=status.HTTP_200_OK)
def get_user(id: UUID4, user_db: USER_DB_Dependancy):
    _, db = user_db
    _service = UserServvice(db)
    return _service.get(id)


@router.delete("/{id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: UUID4, user_db: ADMIN_USER_DB_Dependancy):
    _, db = user_db
    _service = UserServvice(db)
    return _service.delete(id)


@router.patch("/me", status_code=status.HTTP_200_OK)
def update_user(data: UpdateUser, user_db: USER_DB_Dependancy):
    user, db = user_db
    _service = UserServvice(db)
    return _service.update(user.username, data=data)
