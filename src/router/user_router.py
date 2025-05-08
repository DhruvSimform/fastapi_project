from fastapi import APIRouter , Depends , status
from pydantic import UUID4
from sqlalchemy.orm import Session
from ..schemas.user_schema import UserInput,UserOutput 
from ..schemas.auth_schema import Token
from ..service.user_services import UserServvice
from typing import Annotated
from ..dependencies import get_db , get_current_user_and_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


DB_Depndancy = Annotated[Session , Depends(get_db)]

USER_DB_Dependancy = Annotated[tuple[UserOutput, Session], Depends(get_current_user_and_db)]

@router.post("",status_code=status.HTTP_201_CREATED , response_model=UserOutput)
def create_user(data: UserInput, db: DB_Depndancy):
    _service = UserServvice(db)
    return _service.create(data)

@router.get("", response_model= list[UserOutput] , status_code=status.HTTP_200_OK)
def get_users(user_db: USER_DB_Dependancy):
    user , db = user_db
    print(user)
    _service = UserServvice(db)
    return _service.get_all()

@router.get("/{id}", response_model=UserOutput, status_code= status.HTTP_200_OK)
def get_user(id: UUID4,user_db: USER_DB_Dependancy):
    _ , db = user_db
    _service = UserServvice(db)
    return _service.get(id)

