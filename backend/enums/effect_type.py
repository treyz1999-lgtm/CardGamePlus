from enum import Enum

"""
EffectType Enumeration

Defines the valid effect types that can be attached to a Card.

Using an enumeration ensures that only valid effect types are used
throughout the application, improving consistency, readability,
and reducing errors caused by misspelled strings.

Not every EffectType is implemented in V1.
Additional EffectTypes are included so the
game can be expanded without changing the
underlying architecture.
"""

class EffectType(Enum):
    RANK_UP = 'Rank Up'
    HEAL = 'Heal'
    DRAW_CARD = 'Draw Card'
    SEARCH_DECK = 'Search Deck'
    STUN = 'Stun'