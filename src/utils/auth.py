from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException

from ..config.settings import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = settings.REFRESH_TOKEN_EXPIRE_MINUTES


def _genrate_token(data: dict, expires_time: int = 10):
    to_encode = data.copy()

    # Fixing the datetime call and converting to a Unix timestamp
    expire = datetime.now() + timedelta(minutes=expires_time)
    to_encode.update({"exp": int(expire.timestamp())})  # Convert to Unix timestamp

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def create_access_token(data: dict):
    return _genrate_token(data, ACCESS_TOKEN_EXPIRE_MINUTES)


def create_refresh_token(data: dict):
    return _genrate_token(data, REFRESH_TOKEN_EXPIRE_MINUTES)


def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
