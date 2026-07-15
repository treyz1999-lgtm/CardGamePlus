from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from database.database import get_db

from schemas.auth import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    TokenResponse,
)

from services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=RegisterResponse,
)
def register(
    request: RegisterRequest,
    session: Session = Depends(get_db),
) -> RegisterResponse:
    """
    Register a new user account.
    """

    auth_service = AuthService(session)

    auth_service.register(
        username=request.username,
        password=request.password,
    )

    return RegisterResponse(
        message="Registration successful.",
    )


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    request: LoginRequest,
    session: Session = Depends(get_db),
) -> TokenResponse:
    """
    Authenticate a user and return a JWT.
    """

    auth_service = AuthService(session)

    token = auth_service.login(
        username=request.username,
        password=request.password,
    )

    return TokenResponse(
        access_token=token,
    )