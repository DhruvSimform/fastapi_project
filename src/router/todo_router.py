from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..dependencies import get_current_user_and_db
from ..schemas.toso_shcema import TodoInput, TodoOutput, TodoUpdate
from ..schemas.user_schema import UserDetailedOutput
from ..service.todo_services import TodoServices

USER_DB_Dependancy = Annotated[
    tuple[UserDetailedOutput, Session], Depends(get_current_user_and_db)
]

router = APIRouter(prefix="/todo", tags=["todo"])


@router.get("/{id}", response_model=TodoOutput, status_code=status.HTTP_200_OK)
def get_single_todo(id: int, user_db: USER_DB_Dependancy) -> TodoOutput:

    user, db = user_db
    _services = TodoServices(db)
    return _services.get_single_todo_by_user(user.id, id)


@router.get("/", response_model=list[TodoOutput], status_code=status.HTTP_200_OK)
def list_of_todo(user_db: USER_DB_Dependancy) -> list[TodoOutput]:

    user, db = user_db
    _services = TodoServices(db)
    return _services.get_list_of_todo_by_user(user.id)


@router.post("/", response_model=TodoOutput, status_code=status.HTTP_201_CREATED)
def create(data: TodoInput, user_db: USER_DB_Dependancy) -> TodoOutput:

    user, db = user_db
    _services = TodoServices(db)
    return _services.create_todo_for__user(user.id, data)


@router.patch("/{id}", response_model=TodoOutput, status_code=status.HTTP_200_OK)
def update_todo(id: int, data: TodoUpdate, user_db: USER_DB_Dependancy):
    user, db = user_db
    _services = TodoServices(db)
    return _services.update_todo(user.id, id, data)


@router.delete("/{id}", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: int, user_db: USER_DB_Dependancy) -> TodoOutput:

    user, db = user_db
    _services = TodoServices(db)
    return _services.delete_todo(user.id, id)
