from enum import Enum

"""
Condition Enumerations

Defines the valid attributes and comparison operators used to
build Conditions throughout the application.

ConditionAttribute specifies what piece of game state should
be evaluated (such as a card's base rank or a player's health).

Comparison specifies how that value should be evaluated
(Equal, Less Than, Greater Than, etc.).

Using enumerations ensures that Conditions are built from a
consistent, predefined vocabulary, improving readability,
type safety, and reducing errors caused by invalid values.
"""

class ConditionAttribute(Enum):
    BASE_RANK = 'Base Rank'
    HEALTH = 'Health'
    SUIT = 'Suit'
    HAND_SIZE = 'Hand Size'
    PLAYER_HP = 'Player HP'
    OPPONENT_HP = 'Opponent HP'

class Comparison(Enum):
    EQUAL = "Equal"
    LESS_THAN = "Less Than"
    GREATER_THAN = "Greater Than"
    LESS_EQUAL = "Less Than or Equal"
    GREATER_EQUAL = "Greater Than or Equal"
    NOT_EQUAL = "Not Equal"