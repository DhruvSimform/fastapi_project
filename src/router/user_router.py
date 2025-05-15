from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Body, Depends, status
from fastapi.responses import JSONResponse
from pydantic import UUID4
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from ..dependencies import (get_admin_user_and_db, get_current_user_and_db,
                            get_db)
from ..schemas.auth_schema import Token
from ..schemas.user_schema import (UpdateUser, UserDetailedOutput, UserInput,
                                   UserOutput)
from ..service.users_services import UserService
from ..utils.email import send_welcome_email

router = APIRouter(prefix="/users", tags=["Users"])


DB_Depndancy = Annotated[AsyncSession, Depends(get_db)]  # Async DB session

USER_DB_Dependancy = Annotated[
    tuple[UserDetailedOutput, AsyncSession], Depends(get_current_user_and_db)
]

ADMIN_USER_DB_Dependancy = Annotated[
    tuple[UserDetailedOutput, AsyncSession], Depends(get_admin_user_and_db)
]


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=UserDetailedOutput,
    summary="Register a new user",
    description="Creates a new user account with the provided user input.",
    response_description="Details of the newly created user.",
)
async def create_user(
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
    return await _service.create(data)


@router.get(
    "",
    status_code=status.HTTP_200_OK,
    response_model=list[UserOutput | UserDetailedOutput],
    summary="Get all users",
    description="Fetch a list of all users. Accessible based on user role.",
    response_description="A list of users.",
)
async def get_users(user_db: USER_DB_Dependancy, background_tasks: BackgroundTasks):
    user, db = user_db
    _service = UserService(db)
    return await _service.get_all(user.role)


@router.patch(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserDetailedOutput,
    summary="Update current user",
    description="Update the profile details of the currently authenticated user.",
    response_description="Updated user profile information.",
)
async def update_user(data: UpdateUser, user_db: USER_DB_Dependancy):
    user, db = user_db
    _service = UserService(db)
    return await _service.update_user(user.username, data=data)


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    response_model=UserDetailedOutput,
    summary="Get current user profile",
    description="Retrieve the profile information of the currently authenticated user.",
    response_description="Detailed user profile.",
)
async def get_profile_details(user_db: USER_DB_Dependancy):
    user, db = user_db
    _service = UserService(db)
    print(user.id)
    return await _service.get(user.id)


@router.get(
    "/profile/{username}",
    response_model=UserDetailedOutput | UserOutput,
    status_code=status.HTTP_200_OK,
    summary="Get user by username",
    description="Fetch a user's profile by their username. Access depends on requester’s role.",
    response_description="User profile matching the given username.",
)
async def get_user_username(username: str, user_db: USER_DB_Dependancy):
    user, db = user_db
    _service = UserService(db)
    return await _service.get_by_username(user.role, username)


@router.get(
    "/{id}",
    response_model=UserDetailedOutput,
    status_code=status.HTTP_200_OK,
    summary="(Deprecated) Get user by ID",
    description="Retrieve user details using their UUID. This endpoint is deprecated.",
    response_description="User details for the given ID.",
    deprecated=True,
)
async def get_user_by_id(id: UUID4, user_db: USER_DB_Dependancy):
    _, db = user_db
    _service = UserService(db)
    return await _service.get(id)


@router.delete(
    "/{id}",
    response_model=None,
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description="Deletes a user by ID. Only accessible to admins.",
    response_description="No content returned after successful deletion.",
)
async def delete_user(id: UUID4, user_db: ADMIN_USER_DB_Dependancy):
    _, db = user_db
    _service = UserService(db)
    await _service.delete_user(id)
