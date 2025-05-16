import jwt
from fastapi import Request
from slowapi import Limiter

from ..config.settings import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


def hybrid_key_func(request: Request):
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("sub")
            if user_id:
                return f"user:{user_id}"
        except Exception:
            pass  # fall back to IP
    return f"ip:{request.client.host}"


# Initialize limiter with custom key function
limiter = Limiter(
    key_func=hybrid_key_func,
    default_limits=["100/minute"],
)
