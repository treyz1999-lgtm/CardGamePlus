from models.card import Card

"""
Field Model

Represents a player's field during a single game.

The Field acts as the game zone containing all Card objects
currently in play. Cards enter the field when played and
remain there until removed by the GameEngine.

The Field is responsible only for managing the cards it owns
and deriving information about those cards. It does not
determine when gameplay events occur or where cards move next.

Initialized Attributes
----------------------
- cards
    A list of Card objects currently in play.
    Initialized as an empty list.

Field Responsibilities
----------------------
A Field is responsible for:

- Storing cards currently in play.
- Adding cards to the field.
- Removing cards from the field.
- Reporting which cards are in play.
- Reporting how many cards are in play.
- Determining whether a card exists on the field.
- Calculating derived information such as total combat power.
- Applying damage to all cards on the field when instructed.
- Identifying defeated cards after damage has been applied.

A Field is NOT responsible for:

- Deciding when cards are played.
- Resolving combat.
- Moving cards to other game zones.
- Executing card effects.
- Determining turn order.
- Enforcing game rules.
"""


class Field:
    def __init__(self, cards: list[Card] | None = None): #start with an empty field zone unless there is already one given, this will typically not be the case
        self.cards = [] if cards is None else cards

    @property
    def field_size(self) -> int:
        return len(self.cards)

    @property
    def combat_power(self) -> int:
        return sum(card.combat_rank() for card in self.cards)


    def add_cards(self, cards: list[Card]) -> None: #take a list of Card objects and add it to our Field zone
        self.cards.extend(cards)

    def remove_card(self, card: Card) -> Card: #this will allow the Field to move a card out of its zone so the game engine can put it wherever it needs to go afterward
        self.cards.remove(card)
        return card #we don't want to lose the Card object so we return it so that the engine can take it and do what it needs to with it

    def damage_all_cards(self, damage: int = 1) -> None:
        for card in self.cards:
            card.take_damage(damage)

    def defeated_cards(self) -> list[Card]:
        return [card for card in self.cards if card.health <= 0]
