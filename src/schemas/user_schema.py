from datetime import datetime
from uuid import UUID
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)

from ..config.constant import UserRole
from ..utils.password_helper import validate_password


class User(BaseModel):
    """Base model for user schema configuration."""
    model_config = {"from_attributes": True}


class UserInput(User):
    """Schema for user registration."""

    username: str = Field(
        ...,
        title="Username",
        description="Unique username without spaces.",
        example="dhruv",
        min_length=3,
        max_length=32,
    )
    email: EmailStr = Field(
        ...,
        title="Email Address",
        description="Valid email address for the user.",
        example="dhruv@gmail.com",
    )
    password: str = Field(
        ...,
        min_length=8,
        title="Password",
        description="Password must contain at least 8 characters, including a letter, number, and special character.",
        example="P@ssw0rd!"
    )
    confirm_password: str = Field(
        ...,
        title="Confirm Password",
        description="Re-enter the password for confirmation.",
        example="P@ssw0rd!"
    )
    role: UserRole = Field(
        default=UserRole.user,
        title="User Role",
        description="Role of the user. Either 'user' or 'admin'.",
        examples=["admin", "user"]
    )
    first_name: str | None = Field(
        None,
        title="First Name",
        description="User's first name (optional).",
        example="John"
    )
    last_name: str | None = Field(
        None,
        title="Last Name",
        description="User's last name (optional).",
        example="Doe"
    )
    bio: str | None = Field(
        None,
        title="Bio",
        description="A short bio about the user (optional).",
        example="Tech enthusiast and blogger."
    )

    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        if " " in v:
            raise ValueError("Username cannot contain spaces.")
        return v

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not validate_password(v):
            raise ValueError("Password must contain a letter, number, and special character.")
        return v

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Password and Confirm Password must match.")
        return self


class UserLogin(User):
    """Schema for user login."""

    username: str = Field(
        ...,
        title="Username",
        description="Username of the user.",
        example="johndoe_123"
    )
    password: str = Field(
        ...,
        title="Password",
        description="User's password.",
        example="P@ssw0rd!"
    )


class UserInDb(User):
    """Schema representing the user stored in the database."""

    id: UUID
    username: str
    email: EmailStr
    hashed_password: str
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    role: UserRole = UserRole.user
    profile_picture_url: str | None = None
    last_login: datetime | None = None
    created_at: datetime
    # updated_at: datetime | None = None


class UserOutput(User):
    """Public-facing user schema."""

    username: str = Field(
        ...,
        title="Username",
        description="Username of the user.",
        example="johndoe_123"
    )
    email: EmailStr = Field(
        ...,
        title="Email Address",
        description="Email address of the user.",
        example="johndoe@example.com"
    )
    full_name: str | None = Field(
        None,
        title="Full Name",
        description="Full name of the user (optional).",
        example="John Doe"
    )
    bio: str | None = Field(
        None,
        title="Bio",
        description="A short bio about the user (optional).",
        example="Software engineer and open-source contributor."
    )


class UserDetailedOutput(UserOutput):
    """Detailed user response for profile or admin view."""
    id: UUID = Field(
        ...,
        title="User ID",
        description="Unique identifier for the user.",
        example="123e4567-e89b-12d3-a456-426614174000"
    )
    role: str = Field(
        ...,
        title="User Role",
        description="Role of the user, e.g., 'user' or 'admin'.",
        example="admin"
    )
    last_login: datetime | None = Field(
        None,
        title="Last Login",
        description="Timestamp of the user's last login (optional).",
        example="2023-01-01T12:00:00"
    )


class UpdateUser(User):
    """Schema for updating a user's profile."""

    first_name: str | None = Field(
        None,
        title="First Name",
        description="New first name (optional).",
        example="Johnny"
    )
    last_name: str | None = Field(
        None,
        title="Last Name",
        description="New last name (optional).",
        example="Doestar"
    )
    bio: str | None = Field(
        None,
        title="Bio",
        description="Updated bio (optional).",
        example="Full-stack developer based in NY."
    )
