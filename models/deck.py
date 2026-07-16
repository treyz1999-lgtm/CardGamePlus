from models.card import Card
import random
from models.search_criteria import SearchCriteria

"""
Deck Model

Represents a collection of Card objects that a Player uses
throughout a game.

The Deck is responsible for storing, organizing, and providing
access to cards. It manages operations such as drawing,
shuffling, searching, adding, and removing cards, but does not
implement the rules of gameplay.


Required Attributes
-------------------
- cards
    A list of Card objects currently contained in the deck.

- deck_size - this a derived property of the deck
    The intended number of cards in the deck.

    For V1, a valid deck must contain between
    40 and 52 cards (inclusive).

Deck Responsibilities
---------------------
A Deck is responsible for:

- Storing Card objects.
- Validating deck size.
- Drawing cards.
- Shuffling cards.
- Searching for cards.
- Adding cards.
- Removing cards.
- Reporting the number of cards remaining.

A Deck is NOT responsible for:

- Determining turn order.
- Resolving combat.
- Executing card effects.
- Tracking player health.
- Managing game state.
- Saving itself to the database.
"""

class Deck:
    MIN_SIZE = 40 #these might be moved to a config or settings file later
    MAX_SIZE = 52

    def __init__(self, cards: list[Card]) -> None:
        self.cards = cards

    #these are things a deck can derive about itself with no extra input or data required
    @property
    def deck_size(self) -> int:
        return len(self.cards)

    @property
    def is_valid(self) -> bool:
        """Return True if this deck satisfies the game's deck-building rules."""
        return self.MIN_SIZE <= self.deck_size <= self.MAX_SIZE

    #these will be actions that a deck can do to itself
    def shuffle(self) -> None:
        """Randomly shuffle the deck."""
        random.shuffle(self.cards)

    def draw(self, amount : int =1) -> list[Card]: #draw 1 by default, however larger draws can be passed in
        """Remove and return up to `amount` cards from the top of the deck."""
        drawn_cards = []
        if amount < 1:
            raise ValueError("Must draw at least one card.")
        for _ in range(amount):
            if self.deck_size == 0: #this means the deck can draw until it is empty then it will stop
                break
            drawn_cards.append(self.cards.pop(0))
            # A deque would provide O(1) front removals via popleft(), but with a
            # maximum deck size of 52 cards the performance benefit is negligible.
            # A list keeps the implementation simpler.
        return drawn_cards

    def search(self,criteria : SearchCriteria) -> list[Card]:
        """
        Return all cards matching the given search criteria.
            For every Card in the Deck

                Assume it matches.

                If a suit was requested,
                    compare the suit.

                If a rank was requested,
                    compare the rank.

                If an effect was requested,
                    determine whether ANY Effect on the Card
                    has the requested EffectType.

                If the Card still matches,
                    add it to the results.
        """
        results: list[Card] = []
        for card in self.cards:
            match = True
            if criteria.suit is not None:
                if card.suit != criteria.suit:
                    match = False
            if criteria.rank is not None:
                if card.rank != criteria.rank:
                    match = False
            if criteria.effect is not None:
                if not any(
                        effect.effect_type == criteria.effect
                        for effect in card.effects
                ):
                    match = False
            if match:
                results.append(card)
        return results

    def add_card(self, card: Card) -> None:
        self.cards.append(card)

    def add_cards(self, cards: list[Card]) -> None:
        self.cards.extend(cards)

    def remove_card(self, card: Card) -> Card:
        self.cards.remove(card)
        return card

    def peek(self, amount: int = 1) -> list[Card]:
        if amount < 1:
            raise ValueError("Must view at least one card.")
        return self.cards[:amount]

    def contains(self, card: Card) -> bool:
        """Return True if the specified card is in the deck."""
        return card in self.cards

