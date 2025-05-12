from fastapi import HTTPException, status
from pydantic import UUID4
from sqlalchemy.orm import Session

from ..repository.users_repository import UserRepository
from ..schemas.user_schema import (
    UpdateUser,
    UserInput,
    UserOutput,
    UserDetailedOutput,
    UserRole,
)


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def create(self, data: UserInput) -> UserOutput:
        if self.repository.get_user_by_username_or_email(data.username, data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User aleredy exists with this username or email",
            )
        return self.repository.create(data)

    def get_all(self, user_role: UserRole) -> list[UserOutput | UserDetailedOutput]:
        if user_role == UserRole.admin:
            return self.repository.get_all_users_admin()
        return self.repository.get_all_users()

    def get(self, _id: UUID4) -> UserDetailedOutput:
        if not self.repository.user_exists_by_id(_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not exists"
            )

        return self.repository.get_user(_id)
    
    def get_by_username(self, current_user_role: UserRole,_username: str) -> UserOutput | UserDetailedOutput:
        if not self.repository.user_exists_by_username(_username):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not exists"
            )
        
        if current_user_role == UserRole.admin:
            return self.repository.get_user_all_detail_by_username(_username)
        return self.repository.get_user_by_username(_username)


    def delete_user(self, _id: UUID4) -> bool:
        if not self.repository.user_exists_by_id(_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not exists"
            )
        return self.repository.delete_user(_id)

    def update_user(self, _username: str, data: UpdateUser) -> UserDetailedOutput:
        return self.repository.update_user(_username, data)
