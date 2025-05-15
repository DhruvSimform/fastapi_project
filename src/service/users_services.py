from fastapi import BackgroundTasks, HTTPException, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from ..repository.users_repository import UserRepository
from ..schemas.user_schema import (UpdateUser, UserDetailedOutput, UserInput,
                                   UserOutput, UserRole)
from ..utils.email import send_welcome_email
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException, status
from fastapi.background import BackgroundTasks

class UserService:
    """Async service layer for user-related business logic."""

    def __init__(self, db: AsyncSession, background_tasks: BackgroundTasks | None = None):
        self.repository = UserRepository(db)
        self.background_tasks = background_tasks

    async def create(self, data: UserInput) -> UserOutput:
        """Create a new user if username or email doesn't already exist."""
        exists = await self.repository.get_user_by_username_or_email(data.username, data.email)
        if exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists with this username or email",
            )
        result = await self.repository.create(data)
        if self.background_tasks:
            self.background_tasks.add_task(send_welcome_email, result.email, result.username)
        return result

    async def get_all(self, user_role: UserRole) -> list[UserOutput | UserDetailedOutput]:
        """Retrieve all users, detailed for admin."""
        if user_role == UserRole.admin:
            return await self.repository.get_all_users_admin()
        return await self.repository.get_all_users()

    async def get(self, _id: UUID4) -> UserDetailedOutput:
        """Get user details by ID."""
        exists = await self.repository.user_exists_by_id(_id)
        if not exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not exists",
            )
        return await self.repository.get_user(_id)

    async def get_by_username(
        self, current_user_role: UserRole, _username: str
    ) -> UserOutput | UserDetailedOutput:
        """Get user details by username."""
        exists = await self.repository.user_exists_by_username(_username)
        if not exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not exists",
            )

        if current_user_role == UserRole.admin:
            return await self.repository.get_user_all_detail_by_username(_username)
        return await self.repository.get_user_by_username(_username)

    async def delete_user(self, _id: UUID4) -> bool:
        """Delete a user by ID."""
        exists = await self.repository.user_exists_by_id(_id)
        if not exists:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not exists",
            )
        return await self.repository.delete_user(_id)

    async def update_user(self, _username: str, data: UpdateUser) -> UserDetailedOutput:
        """Update user details."""
        return await self.repository.update_user(_username, data)

