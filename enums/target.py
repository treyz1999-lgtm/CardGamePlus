from enum import Enum

"""
Target Enumeration

Defines the valid targets that an Effect may be applied to.

Using an enumeration ensures that effects can only target
predefined game entities, improving consistency and reducing
errors caused by invalid target names.
Only a subset of Targets are used in V1.
Additional Targets are defined so more
complex Effects can be added in future
versions without changing the API.
"""

class Target(Enum):
    SELF = "Self"
    OPPONENT = "Opponent"
    ALLY = "Ally"
    ALL_ALLIES = "All Allies"
    ALL_OPPONENTS = "All Opponents"
    ALL_CARDS = "All Cards"
    PLAYER = "Player"
    OPPONENT_PLAYER = "Opponent Player"