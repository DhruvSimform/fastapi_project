from typing import Annotated, List

from pydantic import UUID4
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..models.user_model import User
from ..schemas.user_schema import (
    UpdateUser,
    UserInput,
    UserOutput,
    UserDetailedOutput,
)
from ..utils.password_helper import get_password_hash


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, data: UserInput) -> UserDetailedOutput:
        user = User(
            **data.model_dump(exclude={"password", "confirm_password"}),
            hash_password=get_password_hash(data.password),
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def get_all_users_admin(self) -> list[UserDetailedOutput]:
        return self.db.query(User).all()

    def get_all_users(self) -> list[UserOutput]:
        # stmt = select(User.username, User.email,User.bio ,  User.first_name , User.last_name )
        # results = self.db.execute(stmt).mappings().all()
        return self.db.query(
            User.username, User.email, User.bio, User.full_name, User.last_login
        ).all()

    def get_user(self, _id: UUID4) -> UserDetailedOutput | None:
        return self.db.query(User).filter_by(id=_id).first()

    def get_user_by_username(self, _username: str) -> UserOutput | None:
        return self.db.query(User.username, User.email, User.bio, User.full_name, User.last_login).filter_by(username=_username).first()
    
    def get_user_all_detail_by_username(self, _username: str) -> UserDetailedOutput | None:
        return self.db.query(User).filter_by(username=_username).first()

    def get_user_by_username_or_email(
        self, _username: str, _email: str
    ) -> UserOutput | None:
        return self.db.query(User).filter((User.username == _username) | (User.email == _email)).first()

    def user_exists_by_username(self, username: str) -> bool:
        return self.db.query(User).filter_by(username=username).first() is not None

    def user_exists_by_id(self, _id: UUID4) -> bool:
        return self.db.query(User).filter_by(id=_id).first() is not None

    def delete_user(self, _id: UUID4) -> bool:
        user = self.db.query(User).filter_by(id=_id).first()
        self.db.delete(user)
        self.db.commit()
        return True

    def update_user(self, _username: str, data: UpdateUser) -> UserDetailedOutput:
        user_query = self.db.query(User).filter_by(username=_username)
        user = user_query.first()

        update_data = data.model_dump(exclude_unset=True)
        user_query.update(update_data)
        self.db.commit()

        self.db.refresh(user)
        return user
