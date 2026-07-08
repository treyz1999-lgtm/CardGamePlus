
from enums.effect_type import EffectType
from enums.target import Target
from enums.trigger import Trigger

"""
Effect Model

Represents a single effect that can be attached to a Card.

An Effect does not contain the logic for how an effect is executed.
Instead, it stores the information necessary for the EffectEngine
to determine when and how the effect should be applied.

Required Attributes
-------------------
- effect_type
    The type of effect represented.
    Example: Rank Up, Heal, Draw Card.

- trigger
    The event that causes this effect to activate.
    Example: On Play, On Draw, After Combat.

- target
    Specifies what object the effect should affect.
    Example: Self, Opponent, All Cards.

- value
    Numeric value associated with the effect.
    Example: +2 Rank, Heal 5 HP.

Optional Attributes
-------------------
- condition
    Optional requirement that must be satisfied before
    the effect can activate.

- description
    Human-readable text describing the effect.
    Used for UI and debugging.

    Effect Responsibilities
-----------------------
An Effect is responsible for:

- Storing effect information.
- Describing what an effect does.
- Providing effect data to the EffectEngine.

An Effect is NOT responsible for:

- Executing game logic.
- Modifying Cards or Players.
- Determining if an effect should activate.
- Managing game state.
- Saving itself to the database.
"""

class Effect:
    def __init__(self, effect_type: EffectType, trigger: Trigger, target: Target, value: int, condition, description):
        pass
