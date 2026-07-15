from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from database.database import get_db
from database.models.user_model import UserModel

from services.user_service import UserService
from services.auth_service import AuthService


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/auth/login",
)


def get_current_user(
    session: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> UserModel:
    """
    Retrieve the authenticated User from a JWT.
    """

    user_service = UserService(session)
    auth_service = AuthService(user_service)

    try:
        payload = auth_service.verify_access_token(token)

        user_id = int(payload["sub"])

        user = user_service.get_by_id(user_id)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials.",
            )

        return user

    except Exception:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials.",
        )