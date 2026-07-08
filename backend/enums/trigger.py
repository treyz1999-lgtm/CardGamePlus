from enum import Enum

"""
Trigger Enumeration

Defines the valid game events that can activate an Effect.

Using an enumeration ensures that effects can only respond to
predefined game events, improving consistency and reducing
errors caused by invalid trigger names.
"""

class Trigger(Enum): #these might not all be used in V1
    ON_PLAY = 'ON Play'
    ON_DRAW = 'On Draw'
    ON_DISCARD = 'On Discard'
    ON_DEATH = 'On Death'
    ON_HEAL = 'On Heal'
    ON_DAMAGE = 'On Damage'
    TURN_START = 'Turn Start'
    TURN_END = 'Turn End'

