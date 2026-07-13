
from sqlalchemy import Integer, ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database.base import Base

"""
DeckCard database table.

Stores the relationship between Decks and Cards.

This table acts as a join table, allowing a Deck to contain
zero or more Cards and allowing a Card to belong to multiple
Decks.

Each row represents a single Card belonging to a single Deck.

The DeckCardModel does not store Card data or Deck data
directly. Instead, it relates existing DeckModel and CardModel
records through their primary keys.

Attributes
----------
deck_id:
    Foreign key identifying the Deck that owns the relationship.

card_id:
    Foreign key identifying the Card contained within the Deck.
"""

class DeckCardModel(Base):

    __tablename__ = 'deck_cards'

    deck_card_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    deck_id: Mapped[int] = mapped_column(
        ForeignKey('decks.deck_id'),
        nullable= False,
    )

    card_id: Mapped[int] = mapped_column(
        ForeignKey('cards.card_id'),
        nullable=False,
    )