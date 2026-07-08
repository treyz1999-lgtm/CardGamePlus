from enums.suit import Suit
from enums.rank import Rank
from models.effects import Effect

"""
Card Model

Represents a single playable card in the game.

Every card should always contain the following information:

Required Attributes
-------------------
- template_id
    Unique identifier linking this card to a base card template.

- suit
    The card's suit (Hearts, Diamonds, Clubs, Spades, Joker).

- rank
    The card's rank (2-14, Joker, etc.).

- effects
    A list of Effect objects attached to this card.
    This list may be empty.

- name
    Human-readable card name.
    Example: "King of Hearts"

Optional Attributes
-------------------
- description
    Human-readable text shown to the player.
    May be None.

Card Responsibilities
---------------------
A Card is responsible for:

- Storing card information.
- Reporting its combat value.
- Providing access to its effects.
- Representing itself as a string for debugging and readability purposes.

A Card is NOT responsible for:

- Determining combat outcomes.
- Executing effects.
- Knowing which player owns it.
- Saving itself to the database.
- Managing game state.

Design Notes
------------
Cards are intentionally lightweight domain objects.

Game logic, combat resolution, and effect execution are handled by
dedicated engine classes to maintain separation of concerns.
"""


class Card:

    def __init__(self, suit: Suit, rank: Rank, effects: list[Effect] | None = None, description: str | None = None):
        self.suit = suit
        self.rank = rank
        self.effects = effects if effects is not None else []
        self.description = description
        self.name = self._generate_name()

    def _generate_name(self) -> str:
        return f"{self.rank.name.title()} of {self.suit.value}"

    def __str__(self) -> str:
        return self.name


#some test cards
if __name__ == "__main__":
    card1 = Card(Suit.HEARTS, Rank.THREE)
    card2 = Card(Suit.SPADES, Rank.KING)

    print(card1)
    print(card2)