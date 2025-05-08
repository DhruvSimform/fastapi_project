from typing import Annotated, List

from pydantic import UUID4
from sqlalchemy.orm import Session

from ..models.user_model import User
from ..schemas.user_schema import UserInput, UserOutput
from ..utils.password_helper import get_password_hash


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: UserInput) -> UserOutput:
        user = User(
            **data.model_dump(exclude={"password", "confirm_password"}),
            hash_password=get_password_hash(data.password),
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_all(self) -> List[UserOutput]:
        return self.db.query(User).all()

    def get_user(self, _id: UUID4) -> UserOutput | None:
        return self.db.query(User).filter_by(id=_id).first()

    def get_user_by_username(self, _username: str) -> UserOutput | None:
        return self.db.query(User).filter_by(username=_username).first()

    def user_exists_by_username(self, username: str) -> bool:
        return self.db.query(User).filter_by(username=username).first() is not None

    def user_exists_by_id(self, _id: UUID4) -> bool:
        return self.db.query(User).filter_by(id=_id).first() is not None

    def delete_user(self, _id: UUID4) -> bool:
        user = self.db.query(User).filter_by(id=_id).first()
        if not user:
            return False
        self.db.delete(user)
        self.db.commit()
        return True
