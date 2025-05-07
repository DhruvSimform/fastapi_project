from fastapi import APIRouter , Depends , status
from pydantic import UUID4
from sqlalchemy.orm import Session
from ..config.database import get_db
from ..schemas.user_schema import UserInput,UserOutput
from ..service.user_services import UserServvice
from typing import Annotated

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

DB_Depndancy = Annotated[Session , Depends(get_db)]

@router.post("",status_code=status.HTTP_201_CREATED , response_model=UserOutput)
def create_user(data: UserInput, db: DB_Depndancy):
    _service = UserServvice(db)
    return _service.create(data)

@router.get("", response_model= list[UserOutput] , status_code=status.HTTP_200_OK)
def get_users(db: DB_Depndancy):
    _service = UserServvice(db)
    return _service.get_all()

@router.get("/{id}", response_model=UserOutput, status_code= status.HTTP_200_OK)
def get_user(id: UUID4,db: DB_Depndancy):
    _service = UserServvice(db)
    return _service.get(id)

# @router.delete(deprecated=True)
# def a():
#     pass

    