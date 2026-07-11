
from enums.rank import Rank
from enums.suit import Suit
from models.card import Card


"""
Standard Deck

Defines the canonical 52-card deck used throughout the game.

This module acts as the source of truth for all standard playing
cards. Each entry stores only the immutable data required to
construct a Card object.

These templates should NEVER be modified directly.

When a player creates a card, the CardFactory (or equivalent
service) should retrieve the desired template, construct a new
Card object from the stored values, attach any purchased effects,
and return that new Card.

This ensures every playable Card is an independent object while
keeping the template data immutable.
"""

STANDARD_DECK = {
# -------------------------
    # Hearts
    # -------------------------

    "AH": {"rank": Rank.ACE,   "suit": Suit.HEARTS},
    "2H": {"rank": Rank.TWO,   "suit": Suit.HEARTS},
    "3H": {"rank": Rank.THREE, "suit": Suit.HEARTS},
    "4H": {"rank": Rank.FOUR,  "suit": Suit.HEARTS},
    "5H": {"rank": Rank.FIVE,  "suit": Suit.HEARTS},
    "6H": {"rank": Rank.SIX,   "suit": Suit.HEARTS},
    "7H": {"rank": Rank.SEVEN, "suit": Suit.HEARTS},
    "8H": {"rank": Rank.EIGHT, "suit": Suit.HEARTS},
    "9H": {"rank": Rank.NINE,  "suit": Suit.HEARTS},
    "TH": {"rank": Rank.TEN,   "suit": Suit.HEARTS},
    "JH": {"rank": Rank.JACK,  "suit": Suit.HEARTS},
    "QH": {"rank": Rank.QUEEN, "suit": Suit.HEARTS},
    "KH": {"rank": Rank.KING,  "suit": Suit.HEARTS},

    # -------------------------
    # Diamonds
    # -------------------------

    "AD": {"rank": Rank.ACE,   "suit": Suit.DIAMONDS},
    "2D": {"rank": Rank.TWO,   "suit": Suit.DIAMONDS},
    "3D": {"rank": Rank.THREE, "suit": Suit.DIAMONDS},
    "4D": {"rank": Rank.FOUR,  "suit": Suit.DIAMONDS},
    "5D": {"rank": Rank.FIVE,  "suit": Suit.DIAMONDS},
    "6D": {"rank": Rank.SIX,   "suit": Suit.DIAMONDS},
    "7D": {"rank": Rank.SEVEN, "suit": Suit.DIAMONDS},
    "8D": {"rank": Rank.EIGHT, "suit": Suit.DIAMONDS},
    "9D": {"rank": Rank.NINE,  "suit": Suit.DIAMONDS},
    "TD": {"rank": Rank.TEN,   "suit": Suit.DIAMONDS},
    "JD": {"rank": Rank.JACK,  "suit": Suit.DIAMONDS},
    "QD": {"rank": Rank.QUEEN, "suit": Suit.DIAMONDS},
    "KD": {"rank": Rank.KING,  "suit": Suit.DIAMONDS},

    # -------------------------
    # Clubs
    # -------------------------

    "AC": {"rank": Rank.ACE,   "suit": Suit.CLUBS},
    "2C": {"rank": Rank.TWO,   "suit": Suit.CLUBS},
    "3C": {"rank": Rank.THREE, "suit": Suit.CLUBS},
    "4C": {"rank": Rank.FOUR,  "suit": Suit.CLUBS},
    "5C": {"rank": Rank.FIVE,  "suit": Suit.CLUBS},
    "6C": {"rank": Rank.SIX,   "suit": Suit.CLUBS},
    "7C": {"rank": Rank.SEVEN, "suit": Suit.CLUBS},
    "8C": {"rank": Rank.EIGHT, "suit": Suit.CLUBS},
    "9C": {"rank": Rank.NINE,  "suit": Suit.CLUBS},
    "TC": {"rank": Rank.TEN,   "suit": Suit.CLUBS},
    "JC": {"rank": Rank.JACK,  "suit": Suit.CLUBS},
    "QC": {"rank": Rank.QUEEN, "suit": Suit.CLUBS},
    "KC": {"rank": Rank.KING,  "suit": Suit.CLUBS},

    # -------------------------
    # Spades
    # -------------------------

    "AS": {"rank": Rank.ACE,   "suit": Suit.SPADES},
    "2S": {"rank": Rank.TWO,   "suit": Suit.SPADES},
    "3S": {"rank": Rank.THREE, "suit": Suit.SPADES},
    "4S": {"rank": Rank.FOUR,  "suit": Suit.SPADES},
    "5S": {"rank": Rank.FIVE,  "suit": Suit.SPADES},
    "6S": {"rank": Rank.SIX,   "suit": Suit.SPADES},
    "7S": {"rank": Rank.SEVEN, "suit": Suit.SPADES},
    "8S": {"rank": Rank.EIGHT, "suit": Suit.SPADES},
    "9S": {"rank": Rank.NINE,  "suit": Suit.SPADES},
    "TS": {"rank": Rank.TEN,   "suit": Suit.SPADES},
    "JS": {"rank": Rank.JACK,  "suit": Suit.SPADES},
    "QS": {"rank": Rank.QUEEN, "suit": Suit.SPADES},
    "KS": {"rank": Rank.KING,  "suit": Suit.SPADES},
}

def create_standard_card(card_id: str) -> Card:
    """
    Create a new Card from one of the standard deck templates.
    """
    template = STANDARD_DECK[card_id]

    return Card(
        suit=template["suit"],
        rank=template["rank"]
    )


"""
king = create_standard_card("KH")
print(king)
"""