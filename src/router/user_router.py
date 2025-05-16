import json
from typing import Annotated

from fastapi import (APIRouter, BackgroundTasks, Body, Depends, Query, Request,
                     status)
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import UUID4
from sqlalchemy.orm import Session

from ..dependencies import (get_admin_user_and_db, get_current_user_and_db,
                            get_db)
from ..schemas.auth_schema import Token
from ..schemas.pagination_schema import PaginatedResponse, PaginationParams
from ..schemas.user_schema import (UpdateUser, UserDetailedOutput, UserInput,
                                   UserOutput)
from ..service.users_services import UserService


from fastapi_cache.decorator import cache
from ..utils.cache import url_key_builder , user_aware_key_builder
from ..utils.rate_limiter import limiter

router = APIRouter(prefix="/users", tags=["Users"])

DB_Depndancy = Annotated[Session, Depends(get_db)]

USER_DB_Dependancy = Annotated[
    tuple[UserDetailedOutput, Session], Depends(get_current_user_and_db)
]

ADMIN_USER_DB_Dependancy = Annotated[
    tuple[UserDetailedOutput, Session], Depends(get_admin_user_and_db)
]


PAGINATION_QUERY_PARAM = Annotated[PaginationParams, Query()]


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=UserDetailedOutput,
    summary="Register a new user",
    description="Creates a new user account with the provided user input.",
    response_description="Details of the newly created user.",
)
def create_user(
    data: Annotated[
        UserInput,
        Body(
            title="User Input",
            description="Payload to create a new user account.",
        ),
    ],
    db: DB_Depndancy,
    backgroundtask: BackgroundTasks,
):
    _service = UserService(db, backgroundtask)
    return _service.create(data)

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=PaginatedResponse[UserOutput | UserDetailedOutput],
    summary="Get all users with pagination",
    description="Fetch a paginated list of all users. Accessible based on user role.",
    response_description="A paginated list of users.",
)
# @cache(expire=60 , namespace="user-list" , key_builder= url_key_builder)
@limiter.limit("20/minute")
async def get_paginated_users(
    # user_db: USER_DB_Dependancy,
    db : DB_Depndancy,
    request: Request,
    pagination: PaginationParams = Depends(),
):
    # user, db = user_db
    _service = UserService(db)
    return _service.get_all_by_page(
        request=request,
        user_role='user',
        page=pagination.page,
        limit=pagination.limit,
)


@router.get(
    "/all",
    status_code=status.HTTP_200_OK,
    response_model=list[UserOutput | UserDetailedOutput],
    summary="Get all users",
    description="Fetch a list of all users. Accessible based on user role.",
    response_description="A list of users.",
    deprecated=True,
)
def get_users(user_db: USER_DB_Dependancy):
    user, db = user_db
    _service = UserService(db)
    return _service.get_all(user.role)


@router.get(
    "/stream",
    status_code=status.HTTP_200_OK,
    summary="Stream all users",
    description="Efficiently stream all users in a JSON array.",
    response_description="A JSON array of users.",
)
def get_users(db: DB_Depndancy):
    service = UserService(db)

    def user_generator():
        yield "["
        first = True
        for user_obj in service.get_all_stream():
            if not first:
                yield ","
            yield json.dumps(user_obj.dict())
            first = False
        yield "]"

    return StreamingResponse(user_generator(), media_type="application/json")


@router.patch(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserDetailedOutput,
    summary="Update current user",
    description="Update the profile details of the currently authenticated user.",
    response_description="Updated user profile information.",
)
def update_user(data: UpdateUser, user_db: USER_DB_Dependancy):
    user, db = user_db
    _service = UserService(db)
    return _service.update_user(user.username, data=data)


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserDetailedOutput,
    summary="Get current user profile",
    description="Retrieve the profile information of the currently authenticated user.",
    response_description="Detailed user profile.",
)
def get_profile_details(user_db: USER_DB_Dependancy):
    user, db = user_db
    _service = UserService(db)
    print(user.id)
    return _service.get(user.id)


@router.get(
    "/profile/{username}",
    response_model=UserDetailedOutput | UserOutput,
    status_code=status.HTTP_200_OK,
    summary="Get user by username",
    description="Fetch a user's profile by their username. Access depends on requester’s role.",
    response_description="User profile matching the given username.",
)
def get_user_username(username: str, user_db: USER_DB_Dependancy):
    user, db = user_db
    _service = UserService(db)
    return _service.get_by_username(user.role, username)


@router.get(
    "/{id}",
    response_model=UserDetailedOutput,
    status_code=status.HTTP_200_OK,
    summary="(Deprecated) Get user by ID",
    description="Retrieve user details using their UUID. This endpoint is deprecated.",
    response_description="User details for the given ID.",
    deprecated=True,
)
def get_user_by_id(id: UUID4, user_db: USER_DB_Dependancy):
    _, db = user_db
    _service = UserService(db)
    return _service.get(id)


@router.delete(
    "/{id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description="Deletes a user by ID. Only accessible to admins.",
    response_description="No content returned after successful deletion.",
)
def delete_user(id: UUID4, user_db: ADMIN_USER_DB_Dependancy):
    _, db = user_db
    _service = UserService(db)
    return _service.delete_user(id)
