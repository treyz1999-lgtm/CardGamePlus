from enum import Enum

"""
Suit Enumeration

Defines the valid suits that a Card may have.

Using an enumeration ensures that only valid suit values are used
throughout the application, improving consistency and reducing errors
caused by misspelled strings.
"""

class Suit(Enum):
    HEARTS = 'Hearts'
    DIAMONDS = 'Diamonds'
    SPADES = 'Spades'
    CLUBS = 'Clubs'
    JOKER = 'Joker'

    def __str__(self):
        return self.value