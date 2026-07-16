from pydantic import BaseModel, Field


class RegisterRequest(BaseModel):
    """
    Payload sent when registering a new user.
    """

    username: str = Field(
        min_length=3,
        max_length=20,
        description="Username must be between 3 and 20 characters.",
    )

    password: str = Field(
        min_length=8,
        max_length=128,
        description="Password must contain at least 8 characters.",
    )


class RegisterResponse(BaseModel):
    """
    Response returned after successful registration.
    """

    message: str


class LoginRequest(BaseModel):
    """
    Payload sent when logging in.
    """

    username: str = Field(
        min_length=3,
        max_length=20,
        description="Username must be between 3 and 20 characters.",
    )

    password: str = Field(
        min_length=8,
        max_length=128,
        description="Password must contain at least 8 characters.",
    )


class TokenResponse(BaseModel):
    """
    JWT returned after successful authentication.
    """

    access_token: str
    token_type: str = "bearer"