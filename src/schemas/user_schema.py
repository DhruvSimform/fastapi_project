from datetime import datetime

from pydantic import UUID4, BaseModel, EmailStr, field_validator, model_validator

from ..config.constant import UserRole
from ..utils.password_helper import validate_password

from pydantic import Field

class User(BaseModel):

    model_config = {"from_attributes": True}


class UserInput(User):
    username: str = Field(..., description="The username of the user, which must be unique.")
    email: EmailStr = Field(..., description="The email address of the user. Must be valid.")
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long and include at least one letter, one number, and one special character.")
    confirm_password: str = Field(..., description="Password confirmation. Must match the password.")
    role: UserRole = Field(UserRole.user, description="Role of the user. Can be 'admin', 'user'. Default is 'user'.")
    first_name: str | None = Field(None, description="The user's first name (optional).")
    last_name: str | None = Field(None, description="The user's last name (optional).")
    bio: str | None = Field(None, description="The user's bio (optional).")

    @field_validator("username")
    def validate_username_field(cls, value):
        if " " in value:
            raise ValueError("Username cannot contain spaces")
        return value

    @field_validator("password")
    def validate_password_field(cls, value):
        if validate_password(password=value):
            return value
        raise ValueError("Password must be strong")

    @model_validator(mode="after")
    def validate_password_and_confirm_password(self):
        if self.password != self.confirm_password:
            raise ValueError("password and confirm password is not same")
        return self
    


class UserInDb(User):
    id: UUID4
    username: str
    email: EmailStr
    hash_password: str
    first_name: str
    last_name: str
    bio: str | None = None
    role: UserRole | None = UserRole.user
    profile_picture_url: str | None = None
    last_login: datetime | None = None

    created_at: datetime
    # updated_at = datetime


class UserOutput(User):
    username: str
    email: EmailStr
    full_name: str | None = None
    bio: str | None


class UserDetailedOutput(UserOutput):
    id: UUID4
    role: str
    last_login: datetime | None


class UpdateUser(User):
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None


class UserLogin(User):
    username: str
    password: str
