from enum import Enum

"""
Effect Duration Enumeration

Defines how long an Effect remains registered after it
becomes active within the game.

Duration is independent of Trigger.

Trigger determines WHEN an Effect may activate.
Duration determines HOW LONG the Effect remains eligible
to activate.
"""

class EffectDuration(Enum):
    IMMEDIATE = 'Immediate'
    WHILE_IN_PLAY = 'While In Play'