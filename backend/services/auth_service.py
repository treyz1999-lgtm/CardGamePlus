from datetime import datetime, timedelta, UTC

import config

from jose import jwt
from passlib.context import CryptContext
from jose import JWTError
from database.models.user_model import UserModel
from services.user_service import UserService

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

    SECRET_KEY = config.SECRET_KEY
    ALGORITHM = config.JWT_ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES = config.ACCESS_TOKEN_EXPIRE_MINUTES

    pwd_context = CryptContext( schemes=["bcrypt"], deprecated="auto",)

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def register(self, username: str,password: str,) -> UserModel:
        """
        Register a new user.

        Workflow
        --------
        1. Verify the username is available.
        2. Hash the user's password.
        3. Delegate user creation to the UserService.
        4. Return the created user.
        """
        existing_user = self.user_service.get_by_username(username)

        if existing_user is not None:
            raise ValueError("Username already exists.")

        hashed_password = self.hash_password(password)

        return self.user_service.create_user( username=username, hashed_password=hashed_password,)

    def login(self, username: str, password: str,) -> str:
        """
        Authenticate an existing user.

        Workflow
        --------
        1. Retrieve the user by username.
        2. Verify the supplied password.
        3. Create a JWT access token.
        4. Return the token.
        """
        user = self.user_service.get_by_username(username)

        if user is None:
            raise ValueError("Invalid username or password.")

        if not self.verify_password(password, user.password_hash,):
            raise ValueError("Invalid username or password.")

        return self.create_access_token(user.user_id)

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

    def create_access_token(self, user_id: int,) -> str:
        """
        Create a JWT access token for an authenticated user.
        """
        expire = datetime.now(UTC) + timedelta(
            minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES
        )

        payload = {
            "sub": str(user_id),
            "exp": expire,
        }

        return jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM,)

    def verify_access_token(self, token: str,) -> dict:
        """
        Verify a JWT access token and return its payload.
        """
        try:
            return jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM],)
        except JWTError:
            raise ValueError("Invalid access token.")