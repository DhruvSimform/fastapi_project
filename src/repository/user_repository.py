from sqlalchemy.orm import Session
from ..models.user_model import User
from ..schemas.user_schema import UserInput,UserOutput
from typing import Annotated , List
from pydantic import UUID4


class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, data: UserInput) -> UserOutput:
        user = User(**data.model_dump() ,hash_passowrd = data.password)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user
    
    def get_all(self) -> List[UserOutput | None]:
        users = self.db.query(User).all()
        return users
    
    def get_user(self,_id: UUID4)-> UserOutput:
        return self.db.query(User).filter_by(id=_id).first()

    def user_exists_by_username(self, username: str) -> bool:
        user = self.db.query(User).filter_by(username = username).first()

        return user is not None
    
    def user_exists_by_id(self, _id: UUID4) -> bool:
        user = self.db.query(User).filter_by(id = _id).first()

        return user is not None
    
    def delete_user(self, _id:UUID4) -> bool:
        user = self.db.query(User).filter_by(id = _id).delete()
        return None
    
    def update():
        pass

        