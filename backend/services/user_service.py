

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

    def create_user(
        self,
        username: str,
        hashed_password: str,
    ):
        pass

    def get_by_id(
        self,
        user_id: int,
    ):
        pass

    def get_by_username(
        self,
        username: str,
    ):
        pass

    def update_gold(
        self,
        user_id: int,
        amount: int,
    ):
        pass

    def delete_user(
        self,
        user_id: int,
    ):
        pass