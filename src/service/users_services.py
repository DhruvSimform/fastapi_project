from fastapi import HTTPException, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from ..repository.users_repository import UserRepository
from ..schemas.user_schema import (
    UpdateUser,
    UserDetailedOutput,
    UserInput,
    UserOutput,
    UserRole,
)


class UserService:
    """Service layer for handling user-related business logic."""

    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def create(self, data: UserInput) -> UserOutput:
        """Create a new user if username or email doesn't already exist."""
        if self.repository.get_user_by_username_or_email(data.username, data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User aleredy exists with this username or email",
            )
        return self.repository.create(data)

    def get_all(self, user_role: UserRole) -> list[UserOutput | UserDetailedOutput]:
        """Retrieve all users, with extra details if the requester is an admin."""
        if user_role == UserRole.admin:
            return self.repository.get_all_users_admin()
        return self.repository.get_all_users()

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
