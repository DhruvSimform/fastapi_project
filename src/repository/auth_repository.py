from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import select

from ..models.user_model import User
from ..schemas.user_schema import UserDetailedOutput, UserLogin
from ..utils.password_helper import verify_password


class AuthRepository:
    """
    Repository class for handling authentication-related database operations.
    Provides methods for user authentication and updating login details.
    """

    def __init__(self, db: Session):
        self.db = db

    async def authenticate_user(self, data: UserLogin) -> UserDetailedOutput | bool:
        result = await self.db.execute(select(User).filter_by(username=data.username))
        user = result.scalar_one_or_none()
        if not user or not verify_password(data.password, user.hash_password):
            return False
        user.last_login = datetime.now()
        await self.db.commit()
        return user
