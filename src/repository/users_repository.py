from typing import Annotated, List

from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models.user_model import User
from ..schemas.user_schema import (UpdateUser, UserDetailedOutput, UserInput,
                                   UserOutput)
from ..utils.password_helper import get_password_hash


from sqlalchemy.future import select
from sqlalchemy import update, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession

class UserRepository:
    """
    UserRepository provides async methods to interact with the User table.
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: UserInput) -> UserDetailedOutput:
        """Create a new user and return the user object."""
        user = User(
            **data.model_dump(exclude={"password", "confirm_password"}),
            hash_password=get_password_hash(data.password),
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def get_all_users_admin(self) -> list[UserDetailedOutput]:
        """Get all users with full details."""
        result = await self.db.execute(select(User))
        users = result.scalars().all()
        return users

    async def get_all_users(self) -> list[UserOutput]:
        """Get all users with limited fields."""
        result = await self.db.execute(
            select(
                User.username, User.email, User.bio, User.full_name, User.last_login
            )
        )
        users = result.all()
        return users

    async def get_user(self, _id: UUID4) -> UserDetailedOutput | None:
        """Get a user by ID."""
        result = await self.db.execute(select(User).filter_by(id=_id))
        user = result.scalar_one_or_none()
        return user

    async def get_user_by_username(self, _username: str) -> UserOutput | None:
        """Get a user by username with limited fields."""
        result = await self.db.execute(
            select(
                User.username, User.email, User.bio, User.full_name, User.last_login
            ).filter_by(username=_username)
        )
        user = result.first()
        return user

    async def get_user_all_detail_by_username(
        self, _username: str
    ) -> UserDetailedOutput | None:
        """Get full user details by username."""
        result = await self.db.execute(select(User).filter_by(username=_username))
        user = result.scalar_one_or_none()
        return user

    async def get_user_by_username_or_email(
        self, _username: str, _email: str
    ) -> UserOutput | None:
        """Get user by username or email."""
        result = await self.db.execute(
            select(User).filter(
                or_(User.username == _username, User.email == _email)
            )
        )
        user = result.scalar_one_or_none()
        return user

    async def user_exists_by_username(self, username: str) -> bool:
        """Check if user exists by username."""
        result = await self.db.execute(select(User).filter_by(username=username))
        return result.scalar_one_or_none() is not None

    async def user_exists_by_id(self, _id: UUID4) -> bool:
        """Check if user exists by ID."""
        result = await self.db.execute(select(User).filter_by(id=_id))
        return result.scalar_one_or_none() is not None

    async def delete_user(self, _id: UUID4) -> bool:
        """Delete a user by ID."""
        await self.db.execute(delete(User).filter_by(id=_id))
        await self.db.commit()
        return True

    async def update_user(self, _username: str, data: UpdateUser) -> UserDetailedOutput | None:
        """Update user data by username."""
        update_data = data.model_dump(exclude_unset=True)
        await self.db.execute(update(User).filter_by(username=_username).values(**update_data))
        await self.db.commit()

        result = await self.db.execute(select(User).filter_by(username=_username))
        user = result.scalar_one_or_none()
        return user

