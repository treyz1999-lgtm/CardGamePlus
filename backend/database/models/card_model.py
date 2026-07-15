from sqlalchemy import Integer, ForeignKey
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database.base import Base


class CardModel(Base):
    """
        Stores the persistent information required to reconstruct
        a runtime Card object.

        Effects are not stored directly in this table.

        Instead, EffectModel records reference the Card using
        card_id, allowing a Card to own zero or more Effects.
    """

    __tablename__ = "cards"

    card_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.user_id'),
        nullable=False,
    )

    suit: Mapped[str] = mapped_column( #this will hold a string like 'HEARTS' or another suit enum name, and can not be null on the DB
        String,
        nullable=False,
    )

    rank: Mapped[int] = mapped_column( #this will hold an int that is the value of the Rank enum, so we don't store like ACE here instead we store 14, can not be null on the DB
        Integer,
        nullable=False,
    )
    health: Mapped[int] = mapped_column( 
        Integer,
        nullable=False,
        default=1,
    )

    def __init__(
            self,
            user_id: int,
            suit: str,
            rank: int,
            health: int = 1,
    ):
        """
        Initialize a Card database record.

        The database generates the card_id automatically.
        Effects are stored separately and reference this Card
        through its generated card_id.
        """

        self.user_id = user_id
        self.suit = suit
        self.rank = rank
        self.health = health

