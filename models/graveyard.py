from models.card import Card
from models.search_criteria import SearchCriteria

"""
Graveyard Model

Represents a player's graveyard during a single game.

The Graveyard acts as a game zone that stores Card objects which
have left the field. Cards may later be retrieved by game effects,
returned to the deck, or otherwise manipulated by future mechanics.

Unlike the Deck, the Graveyard has no concept of drawing or shuffling
during normal gameplay. It simply manages cards that have been placed
there.

Initialized Attributes
----------------------
- cards
    A list of Card objects currently in the graveyard.
    Initialized as an empty list.

Graveyard Responsibilities
--------------------------
A Graveyard is responsible for:

- Storing defeated or discarded cards.
- Adding cards to the graveyard.
- Removing cards from the graveyard.
- Searching for cards.
- Reporting its current size.
- Determining whether a card exists within it.

A Graveyard is NOT responsible for:

- Determining when cards enter or leave the graveyard.
- Resolving card effects.
- Managing game rules.
- Determining combat outcomes.
- Returning cards to play automatically.
"""

class Graveyard:
    def __init__(self, grave: list[Card] | None = None) -> None:
        self.grave = [] if grave is None else grave

    @property
    def size(self) -> int:
        return len(self.grave)

    def add_cards(self, cards: list[Card]) -> None: #give Graveyard any list of Card objects from anywhere, and it will add them to its list
        self.grave.extend(cards)

    def remove_card(self, card: Card) -> Card: #take a Card from grave and remove it, we return that Card object so that the game engine can determine where to send it
        self.grave.remove(card)
        return card

    def contains(self, card: Card) -> bool: #check if a Card exist within our list, might want to use this in the remove function as validation because we cant remove what we don't already have
        return card in self.grave

    def search(self, criteria: SearchCriteria) -> list[Card]: #this is the same function as Deck but for our Graveyard object instead, might end up as a helper or something later
        results: list[Card] = []
        for card in self.grave:
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

    def peek(self) -> list[Card]: #this function is similar to the Deck peek however the entire Graveyard zone will be exposed to view
        return self.grave.copy() #we will make a copy just to prevent mutations on the actual grave