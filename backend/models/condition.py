from enums.condition import ConditionAttribute, Comparison

"""
Condition Model

Represents a single condition that must evaluate to True
before an Effect can be executed.

A Condition describes what should be checked but does not
contain the logic required to evaluate itself.

Required Attributes
-------------------
- attribute
    The game attribute to evaluate.
    Example: Base Rank, Health, Suit.

- comparison
    The comparison operator used during evaluation.
    Example: Less Than, Equal, Greater Than.

- value
    The value used in the comparison.

Condition Responsibilities
--------------------------
A Condition is responsible for:

- Storing condition information.
- Describing the requirements for an Effect.
- Providing condition data to the ConditionEngine.

A Condition is NOT responsible for:

- Evaluating itself.
- Executing game logic.
- Modifying Cards or Players.
- Managing game state.
"""



class Condition:
    def __init__(self, attribute: ConditionAttribute, comparison: Comparison, value):
        self.attribute = attribute
        self.comparison = comparison
        self.value = value

    def generate_text(self) -> str:
        return (
            f"If {self.attribute.value} "
            f"is {self.comparison.value} "
            f"{self.value}"
        )