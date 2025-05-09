import re

from passlib.context import CryptContext
from pydantic import BaseModel

REG = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
PATTERN = re.compile(REG)


class PasswordIn(BaseModel):
    password: str


class HashPasswordOut(BaseModel):
    hash_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hash_password: str) -> bool:
    return pwd_context.verify(plain_password, hash_password)


def validate_password(password: str) -> bool:
    return re.search(PATTERN, password)
