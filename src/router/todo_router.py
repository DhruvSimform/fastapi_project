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

router = APIRouter(prefix="/todo", tags=["Todo"])


@router.get(
    "/{id}",
    response_model=TodoOutput,
    status_code=status.HTTP_200_OK,
    summary="Get a single TODO",
    description="Retrieve a specific TODO item by its ID for the authenticated user.",
    response_description="The requested TODO item.",
)
def get_single_todo(id: int, user_db: USER_DB_Dependancy) -> TodoOutput:
    user, db = user_db
    _services = TodoServices(db)
    return _services.get_single_todo_by_user(user.id, id)


@router.get(
    "/",
    response_model=list[TodoOutput],
    status_code=status.HTTP_200_OK,
    summary="List all TODOs",
    description="Fetch all TODO items created by the authenticated user.",
    response_description="A list of TODO items.",
)
def list_of_todo(user_db: USER_DB_Dependancy) -> list[TodoOutput]:
    user, db = user_db
    _services = TodoServices(db)
    return _services.get_list_of_todo_by_user(user.id)


@router.post(
    "/",
    response_model=TodoOutput,
    status_code=status.HTTP_201_CREATED,
    summary="Create a TODO",
    description="Create a new TODO item for the authenticated user.",
    response_description="The created TODO item.",
)
def create(data: TodoInput, user_db: USER_DB_Dependancy) -> TodoOutput:
    user, db = user_db
    _services = TodoServices(db)
    return _services.create_todo_for__user(user.id, data)


@router.patch(
    "/{id}",
    response_model=TodoOutput,
    status_code=status.HTTP_200_OK,
    summary="Update a TODO",
    description="Update an existing TODO item by ID for the authenticated user.",
    response_description="The updated TODO item.",
)
def update_todo(id: int, data: TodoUpdate, user_db: USER_DB_Dependancy):
    user, db = user_db
    _services = TodoServices(db)
    return _services.update_todo(user.id, id, data)


@router.delete(
    "/{id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a TODO",
    description="Delete a TODO item by its ID for the authenticated user.",
    response_description="No content returned after successful deletion.",
)
def delete_todo(id: int, user_db: USER_DB_Dependancy):
    user, db = user_db
    _services = TodoServices(db)
    return _services.delete_todo(user.id, id)
