from typing import List

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session
from repository.user_repository import UserRepository
from schemas.user_schema import UserInput,UserOutput

class UserServvice:
    def __init__(self,db: Session):
        self.repository = UserRepository(db)
    
    def create(self, data: UserInput) -> UserOutput:
        pass

