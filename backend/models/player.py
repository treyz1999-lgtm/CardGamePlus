from models.card import Card
from models.deck import Deck
from models.field import Field
from models.graveyard import Graveyard
"""
Player Model

Represents a participant in a single game.

A Player manages the game state associated with one participant,
including their deck, hand, field, graveyard, and current health.

The Player exists only for the duration of a match and is
independent of any user account or database records.

Cards move between different game zones throughout a match.
The Player maintains one of these zones as a list representing
the player's hand.

The Player manages several game zones, including the player's
Deck and Hand. Cards move between these zones as the game
progresses.

Required Attributes
-------------------
- deck
    The Deck used by the player during the match.

Initialized Attributes
----------------------
- hand
    A list of Card objects currently held by the player.
    Initialized as an empty list.

- health
    The player's current health.
    Initialized to the game's starting health.

Player Responsibilities
-----------------------
A Player is responsible for:

- Owning a Deck.
- Owning a Field
- Owning a Graveyard.
- Maintaining the player's hand.
- Drawing cards from the Deck.
- Playing cards from the hand.
- Tracking current health.
- Receiving damage and healing.

A Player is NOT responsible for:

- Resolving combat.
- Executing card effects.
- Managing turn order.
- Enforcing game rules.
- Storing user account information.
- Saving or loading data from a database.

For V1 the Hand is represented as a list of Cards.
A dedicated Hand model may be introduced if additional
hand-specific behavior is required.
"""

class Player:

    MAX_HEALTH = 10
    STARTING_ACTIONS = 1

    @property
    def hand_size(self) -> int:
        return len(self.hand)

    @property
    def is_alive(self) -> bool:
        return self.health > 0

    def __init__(self, deck: Deck):
        self.deck = deck #this deck is a list of Card objects that the Player can move Card objects to and from
        self.hand: list[Card] = [] #the player will always initialize with an empty hand. A hand is similar to a deck however it acts only as a zone where Card objects are stored so really it is just a container that holds objects the player has access to temporarily
        self.field = Field() #create a Field object - the Field is a zone that Card objects cam move to and from, naturally each Player owns a Field
        self.graveyard = Graveyard() #create a Graveyard object - the Field is a zone that Card objects cam move to and from, naturally each Player owns a Graveyard
        self.health = self.MAX_HEALTH #this might later be set to a variable that is in a config or settings file, but for V1 the player will have 10 HP
        self.actions = self.STARTING_ACTIONS

    def add_to_hand(self, cards: list[Card]) -> None: #this function accepts Card(s) regardless of their origin, meaning we use this to add cards from any zone not just the deck
        self.hand.extend(cards)

    def draw_cards(self, amount: int) -> None: #this function is explicitly for adding cards from the deck to the hand using the Deck's draw function which exposes x cards then adding them to the hand zone
        cards = self.deck.draw(amount)
        self.add_to_hand(cards)

    def play_card(self, card: Card) -> None: # Move a Card from the player's hand to their Field. he GameEngine determines when a card is played; the Player performs the movement between its own zones.
        if self.actions <= 0:
            raise ValueError("Player has no remaining actions.")

        if card not in self.hand:
            raise ValueError("Card is not in the player's hand.")

        self.hand.remove(card)
        self.field.add_cards([card])
        self.actions -= 1

    def take_damage(self, damage: int) -> int: #take x damage and then return new health value
        self.health -= damage
        return self.health

    def heal(self, health: int) -> int: #heal x health, the HP cap is 10 so if you get more than that, you are set back to 10. Return new HP amount
        self.health += health
        if self.health > self.MAX_HEALTH:
            self.health = self.MAX_HEALTH

        return self.health

    def reset_actions(self) -> None:
        self.actions = self.STARTING_ACTIONS

    def get_health(self) -> int:
        return self.health

