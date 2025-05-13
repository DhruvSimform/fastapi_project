from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ..repository.auth_repository import AuthRepository
from ..schemas.auth_schema import RefreshToken, Token
from ..schemas.user_schema import UserLogin as AuthInput
from ..utils.auth import create_access_token, create_refresh_token, verify_token


class AuthService:
    """
    AuthService class provides authentication-related services, including user login and token management.
    """
    
    def __init__(self, db: Session):
        self.repository = AuthRepository(db)

    def login_for_token(self, data: AuthInput) -> Token:
        """Authenticate user and generate tokens."""

        user = self.repository.authenticate_user(data)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Username or password is incorrect.",
            )
        access_token = create_access_token(data={"sub": user.username})
        refresh_token = create_refresh_token(data={"sub": user.username})

        # Store the refresh token in the database
        # self.repository.store_refresh_token(user, refresh_token)

        return Token(
            access_token=access_token, refresh_token=refresh_token, token_type="Bearer"
        )

    @staticmethod
    def refresh_access_token(_token: RefreshToken) -> RefreshToken:
        """
        Refreshes the access token and generates a new refresh token using the provided refresh token.
        """

        payload = verify_token(token=_token)

        access_token = create_access_token(data=payload)
        refresh_token = create_refresh_token(data=payload)

        return Token(
            access_token=access_token, refresh_token=refresh_token, token_type="Bearer"
        )
