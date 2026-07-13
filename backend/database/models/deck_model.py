from sqlalchemy import Integer, ForeignKey
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database.base import Base


class DeckModel(Base):
    """
    Deck database table.

    Stores the persistent information required to reconstruct
    a runtime Deck object.

    A Deck belongs to exactly one User.

    The cards contained within a Deck are stored in the
    DeckCardModel join table.
    """

    __tablename__ = "decks"

    deck_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,)

    user_id: Mapped[int] = mapped_column(
        ForeignKey('users.user_id'),
        nullable= False,
    )

    name: Mapped[str] = mapped_column( #they can give it a name but if they don't it will just use its ID
        String,
        nullable=False,
        default =  'New Deck'
    )