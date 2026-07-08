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
    EQUAL = "equal"
    LESS_THAN = "less than"
    GREATER_THAN = "greater than"
    LESS_EQUAL = "less than or equal"
    GREATER_EQUAL = "greater than or equal"
    NOT_EQUAL = "not equal"