from enums.suit import Suit
from enums.rank import Rank
from models.effect import Effect

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

    def __init__(self, suit: Suit, rank: Rank, health: int =1, effects: list[Effect] | None = None, description: str | None = None):
        self.suit = suit
        self.rank = rank
        self.effects = effects if effects is not None else []
        self.description = description
        self.name = self._generate_name()
        self.health = health #by default all cards have 1 health meaning they are destroyed after playing them, but this value can be changed via effects or passing in a higher health parameter for some cards
        self.combat_rank = rank.value #start the numerical value for this Card's rank

    @property
    def is_alive(self)-> bool:
        return self.health > 0

    def _generate_name(self) -> str:
        return f"{self.rank.name.title()} of {self.suit.value}"

    def __str__(self) -> str:
        return self.name

    def get_rank(self) -> int:
        #this will only ever return the base rank of a card
        return self.rank.value

    def get_suit(self) -> Suit:
        return self.suit

    def get_effects(self) -> list[Effect]:
        return self.effects

    def get_health(self) -> int:
        return self.health

    def take_damage(self, damage: int) -> int: #take x damage and then return new health value
        self.health -= damage
        return self.health

    def increase_rank(self, amount: int) -> int:
        self.combat_rank += amount
        return self.combat_rank

    def get_combat_rank(self) -> int:
        return self.combat_rank

    def reset_combat_rank(self) -> None:
        self.combat_rank = self.rank.value


#some test cards
if __name__ == "__main__":
    card1 = Card(Suit.HEARTS, Rank.THREE)
    card2 = Card(Suit.SPADES, Rank.KING)

    print(card1)
    print(card1.get_suit())
    print(card1.get_rank())
    print(card1.get_effects())
    print(card2)
    print(card2.get_suit())
    print(card2.get_rank())
    print(card2.get_effects())
