from enum import Enum

"""
EffectType Enumeration

Defines the valid effect types that can be attached to a Card.

Using an enumeration ensures that only valid effect types are used
throughout the application, improving consistency, readability,
and reducing errors caused by misspelled strings.
"""

class EffectType(Enum): #these might not all be implemented in V1, but this design allows for easy expansion of effects
    RANK_UP = 'Rank Up'
    HEAL = 'Heal'
    DRAW_CARD = 'Draw Card'
    SEARCH_DECK = 'Search Deck'
    STUN = 'Stun'