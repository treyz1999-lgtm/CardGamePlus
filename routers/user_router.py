from fastapi import APIRouter
from fastapi import Depends

from database.models.user_model import UserModel

from dependencies.auth import get_current_user

from schemas.user import UserResponse


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get(
    "/me",
    response_model=UserResponse,
)
def get_current_user_info(
    current_user: UserModel = Depends(get_current_user),
) -> UserResponse:
    """
    Retrieve the currently authenticated User.
    """

    return UserResponse(
        user_id=current_user.user_id,
        username=current_user.username,
        gold=current_user.gold,
    )