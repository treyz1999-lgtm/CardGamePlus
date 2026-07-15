
from pydantic import BaseModel


class UserResponse(BaseModel):
    """
    Persistent user information.
    """

    user_id: int
    username: str
    gold: int