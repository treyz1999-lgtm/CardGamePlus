
from sqlalchemy.orm import Session

from database.models.user_model import UserModel
"""
User Service

Responsible for persisting User records.

Responsibilities
----------------
- Create new users.
- Retrieve existing users.
- Update user information.
- Delete users.
- Update player gold.

The UserService does not perform authentication.
Authentication is delegated to the AuthService.
"""
class UserService:

    def __init__(self, session: Session):
        self.session = session

    def create_user(self, username: str, hashed_password: str,) -> UserModel:
        """
           Create and persist a new user.
           """
        user = UserModel( username=username,password_hash = hashed_password, gold = 0,) #create SQL Alchemy Object

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        return user

    def get_by_id(self, user_id: int,) -> UserModel | None:
        """
           Retrieve a user by ID.
           """

        return (
            self.session.query(UserModel).filter(UserModel.user_id == user_id).first()
        )
    """
    equivalent to:
    SELECT *
    FROM users
    WHERE user_id = x
    LIMIT 1;
    """

    def get_by_username(self, username: str,) -> UserModel | None:
        """
            Retrieve a user by username.
            """

        return (
            self.session.query(UserModel).filter(UserModel.username == username).first()
        )

    def update_gold(self, user_id: int, amount: int,) -> UserModel:
        """
            Add gold to a user's account.
            """

        user = self.get_by_id(user_id)

        if user is None:
            raise ValueError("User not found.")

        user.gold += amount

        self.session.commit()
        self.session.refresh(user)

        return user

    def delete_user(self, user_id: int,)  -> None:
        """
            Delete a user.
            """

        user = self.get_by_id(user_id)

        if user is None:
            raise ValueError("User not found.")

        self.session.delete(user)
        self.session.commit()