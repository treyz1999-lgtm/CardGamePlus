from models.effect import Effect
from models.condition import Condition

from enums.effect_type import EffectType
from enums.trigger import Trigger
from enums.target import Target
from enums.condition import ConditionAttribute, Comparison


def test_effect_description():

    condition = Condition(
        ConditionAttribute.BASE_RANK,
        Comparison.LESS_THAN,
        3
    )

    effect = Effect(
        EffectType.RANK_UP,
        Trigger.ON_PLAY,
        Target.SELF,
        5,
        condition
    )

    print(effect.generate_description())

    assert (
        effect.generate_description()
        == "If Base Rank is less than 3, Increase Self rank by 5."
    )


test_effect_description()