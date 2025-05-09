from pydantic import UUID4, BaseModel, EmailStr, Field, field_validator  , model_validator  ,computed_field
from ..utils.password_helper import validate_password
from datetime import datetime
from enum import Enum


class UserRole(str ,Enum):
    admin = "admin"
    user = "user"

class User(BaseModel):
    class Config:
        orm_mode = True


class UserInput(User):
    username: str
    email: EmailStr
    password: str
    confirm_password: str
    role:UserRole = UserRole.user
    first_name : str | None = None
    last_name: str | None = None
    bio: str | None = None


    @field_validator('username')
    def validate_username_field(cls,value):
        if " " in value:
            raise ValueError("Username cannot contain spaces")
        return value
    
    @field_validator('password')
    def validate_password_field(cls,value):
        if validate_password(password= value):
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
    role: UserRole | None = None
    profile_picture_url : str | None = None
    last_login : datetime | None = None

    created_at: datetime


    class Config:
        orm_mode = True


class UserOutput(User):
    username: str
    email: EmailStr
    bio: str | None
    first_name : str | None
    last_name : str | None


    @computed_field(return_type=str)
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class UserOutputAdmin(UserOutput):
    id: UUID4 
    role:str 
    last_login: datetime | None

class UpdateUser(User):
    username: str | None = None
    email: EmailStr | None = None



class UserLogin(User):
    username: str
    password: str
