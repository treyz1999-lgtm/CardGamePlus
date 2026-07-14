from datetime import datetime, timedelta
from os import getenv

from jose import jwt
from passlib.context import CryptContext


class AuthService:
    """
    Authentication Service

    Responsible for authenticating users and issuing access tokens.

    Responsibilities
    ----------------
    - Register new users.
    - Authenticate existing users.
    - Hash passwords.
    - Verify passwords.
    - Create JWT access tokens.
    - Verify JWT access tokens.

    The AuthService is responsible only for authentication.
    User persistence is delegated to the UserService.
    """

    SECRET_KEY = getenv("SECRET_KEY", "war-plus-development-secret")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60

    pwd_context = CryptContext(
        schemes=["bcrypt"],
        deprecated="auto",
    )

    def register(
        self,
        username: str,
        password: str,
    ):
        """
        Register a new user.

        Workflow
        --------
        1. Verify the username is available.
        2. Hash the user's password.
        3. Delegate user creation to the UserService.
        4. Return the created user.
        """
        pass

    def login(
        self,
        username: str,
        password: str,
    ):
        """
        Authenticate an existing user.

        Workflow
        --------
        1. Retrieve the user by username.
        2. Verify the supplied password.
        3. Create a JWT access token.
        4. Return the token.
        """
        pass

    def hash_password(
        self,
        password: str,
    ) -> str:
        """
        Hash a plaintext password using bcrypt.
        """
        return self.pwd_context.hash(password)

    def verify_password(
        self,
        plain_password: str,
        hashed_password: str,
    ) -> bool:
        """
        Verify a plaintext password against a stored hash.
        """
        return self.pwd_context.verify(
            plain_password,
            hashed_password,
        )

    def create_access_token(
        self,
        user_id: int,
    ) -> str:
        """
        Create a JWT access token for an authenticated user.
        """
        pass

    def verify_access_token(
        self,
        token: str,
    ):
        """
        Verify a JWT access token and return its payload.
        """
        pass