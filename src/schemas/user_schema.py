from pydantic import UUID4, BaseModel, EmailStr, Field, field_validator


class User(BaseModel):
    pass


class UserInput(User):
    username: str
    email: EmailStr
    password: str


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
