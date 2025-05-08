from passlib.context import CryptContext
from pydantic import BaseModel


class PasswordIn(BaseModel):
    password: str


class HashPasswordOut(BaseModel):
    hash_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hash_password: str) -> bool:
    return pwd_context.verify(plain_password, hash_password)
