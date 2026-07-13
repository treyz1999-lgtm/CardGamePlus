
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database.base import Base

"""
User Table

Represents a registered account within the application.

The User table stores persistent account information used by
the application outside of an active game. Each User is assigned
a unique identifier by the database, which is then used to relate
that User to other persistent objects such as Cards, Decks,
and purchased Effects.

The User table is NOT the same as the Player model.

A User represents a permanent account, while a Player is a
temporary runtime object created by the GameEngine whenever a
match begins.

Initialized Columns
-------------------
- user_id
    Database-generated primary key used to uniquely identify
    the User and relate owned data.

- username
    Unique account name chosen during registration.

- password_hash
    Securely hashed password used for authentication.
    Raw passwords are never stored.

- gold
    The User's current gold balance used to purchase
    cards and effects.

- wins
    Total number of matches won.

- losses
    Total number of matches lost.

Responsibilities
----------------
The User table is responsible for storing:

- Account credentials.
- Currency.
- Lifetime statistics.
- Ownership relationships to Cards, Decks, and other
  persistent game objects.

The User table is NOT responsible for storing:

- Active game state.
- Player health.
- Hand contents.
- Field contents.
- Graveyard contents.
- Turn information.
- Runtime engine state.

Relationships
-------------
A User may own:

- Many Cards.
- Many Decks.
- Many purchased Effects.
- Match history (future).

These relationships are established using the User's
database-generated primary key (user_id).
"""

class UserModel(Base):
    """
    User database table.
    """

    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    username: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    gold: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    wins: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    losses: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )
