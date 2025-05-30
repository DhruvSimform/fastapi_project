from typing import Generator

from fastapi import BackgroundTasks, HTTPException, Request, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from ..repository.users_repository import UserRepository
from ..schemas.pagination_schema import PaginatedResponse, PaginationParams
from ..schemas.user_schema import (
    UpdateUser,
    UserDetailedOutput,
    UserInput,
    UserOutput,
    UserRole,
)
from ..utils.email import send_welcome_email


class UserService:
    """Service layer for handling user-related business logic."""

    def __init__(self, db: Session, backroundtask: BackgroundTasks = None):
        self.repository = UserRepository(db)
        self.backroundtask = backroundtask

    def create(self, data: UserInput) -> UserOutput:
        """Create a new user if username or email doesn't already exist."""
        if self.repository.get_user_by_username_or_email(data.username, data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User aleredy exists with this username or email",
            )
        result = self.repository.create(data)
        self.backroundtask.add_task(send_welcome_email, result.email, result.username)
        return result

    def get_all_by_page(
        self, request: Request, user_role: UserRole, page: int, limit: int
    ) -> PaginatedResponse[UserOutput | UserDetailedOutput]:
        """Retrieve all users, with extra details if the requester is an admin."""
        skip = (page - 1) * limit
        total = self.repository.get_total_user_count()
        users = None
        total_pages = (total + limit - 1) // limit

        def build_url(new_page: int) -> str:
            return str(request.url.include_query_params(page=new_page, limit=limit))

        if user_role == UserRole.admin:
            users = self.repository.get_users_paginated_admin(skip=skip, limit=limit)
        else:
            users = self.repository.get_users_paginated(skip=skip, limit=limit)

        return PaginatedResponse[UserDetailedOutput | UserOutput](
            total=total,
            total_pages=total_pages,
            page=page,
            size=limit,
            data=users,
            has_next=page < total_pages,
            has_previous=page > 1,
            next_page_url=build_url(page + 1) if page < total_pages else None,
            previous_page_url=build_url(page - 1) if page > 1 else None,
        )

    def get_all(self, user_role: UserRole) -> list[UserOutput | UserDetailedOutput]:
        """Retrieve all users, with extra details if the requester is an admin."""
        if user_role == UserRole.admin:
            return self.repository.get_all_users_admin()
        return self.repository.get_all_users()

    def get_all_stream(self) -> Generator[UserOutput, None, None]:
        return self.repository.stream_all_users()

    def get(self, _id: UUID4) -> UserDetailedOutput:
        """Get user details by ID if the user exists."""
        if not self.repository.user_exists_by_id(_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not exists"
            )

        return self.repository.get_user(_id)

    def get_by_username(
        self, current_user_role: UserRole, _username: str
    ) -> UserOutput | UserDetailedOutput:
        """Get user details by username with different views for admin and normal users."""
        if not self.repository.user_exists_by_username(_username):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not exists"
            )

        if current_user_role == UserRole.admin:
            return self.repository.get_user_all_detail_by_username(_username)
        return self.repository.get_user_by_username(_username)

    def delete_user(self, _id: UUID4) -> bool:
        """Delete a user by ID if the user exists."""
        if not self.repository.user_exists_by_id(_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not exists"
            )
        return self.repository.delete_user(_id)

    def update_user(self, _username: str, data: UpdateUser) -> UserDetailedOutput:
        """Update user details using their username."""
        return self.repository.update_user(_username, data)
