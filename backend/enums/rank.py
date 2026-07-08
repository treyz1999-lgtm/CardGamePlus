from enum import Enum

"""
Rank Enumeration

Defines the valid card ranks used throughout the game.

Using an enumeration provides a single source of truth for card ranks
and prevents invalid or inconsistent values from being used.
"""

class Rank(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14
    JOKER = 15

    def __str__(self):
        return self.value
