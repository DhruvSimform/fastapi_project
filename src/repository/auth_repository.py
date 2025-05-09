from sqlalchemy.orm import Session

from ..models.user_model import User
from ..schemas.user_schema import UserLogin, UserOutput
from ..utils.password_helper import verify_password
from datetime import datetime

class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def authenticate_user(self, data: UserLogin) -> UserOutput | bool:
        user = self.db.query(User).filter_by(username=data.username).first()
        if not user or not verify_password(data.password, user.hash_password):
            return False
        user.last_login = datetime.now()
        self.db.commit()
        return user

