from pydantic import BaseModel
from pydantic import Field


class UserResponse(BaseModel):
    """
    Persistent User information returned to the frontend.
    """

    user_id: int = Field(
        description="Unique identifier for the authenticated User.",
        examples=[1],
    )

    username: str = Field(
        description="The User's username.",
        examples=["Lewis"],
    )

    gold: int = Field(
        ge=0,
        description="The User's current gold balance.",
        examples=[1500],
    )