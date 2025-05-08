from fastapi import HTTPException , status , Depends
from pydantic import UUID4
from sqlalchemy.orm import Session
from ..repository.user_repository import UserRepository
from ..schemas.user_schema import UserInput,UserOutput , UserLogin
from ..schemas.auth_schema import Token , RefreshToken
from ..utils.auth import create_access_token , create_refresh_token , verify_token
from fastapi.security import OAuth2PasswordBearer

class UserServvice:
    def __init__(self,db: Session):
        self.repository = UserRepository(db)
    
    def create(self, data: UserInput) -> UserOutput:
        if self.repository.user_exists_by_username(data.username):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST , detail="User aleredy exists with this db")
        return self.repository.create(data)
    
    def get_all(self) -> list[UserOutput] | None:
        return self.repository.get_all()
    
    def get(self, _id: UUID4) -> UserOutput:
        return self.repository.get_user(_id)
    
    def delete(self, _id: UUID4) -> bool:
        if not self.repository.user_exists_by_id(_id):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail="User not exists")
    
    def updae():
        pass

    
    def login_for_token(self, data: UserLogin) -> Token:
        user = self.repository.authenticate_user(data)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Use a unique and serializable field in JWT payload

        access_token = create_access_token(data={"sub": user.username})
        refresh_token = create_refresh_token(data={"sub": user.username})

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer"
        )
    
    @staticmethod
    def genrate_new_access_token(_token: RefreshToken):
        payload = verify_token(token=_token)

        access_token = create_access_token(data=payload)
        refresh_token = create_refresh_token(data=payload)

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="Bearer"
        )
        


