from pydantic import UUID4, BaseModel, EmailStr, Field, field_validator  , model_validator
from ..utils.password_helper import validate_password


class User(BaseModel):
    pass


class UserInput(User):
    username: str
    email: EmailStr
    password: str
    confirm_password: str

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

    class Config:
        orm_mode = True


class UserOutput(User):
    id: UUID4
    username: str
    email: EmailStr


class UpdateUser(User):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserLogin(User):
    username: str
    password: str
