from enums.effect_duration import EffectDuration
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
        effect_type=EffectType.HEAL,
        trigger=Trigger.ON_PLAY,
        target=Target.SELF,
        value=2,
        duration=EffectDuration.IMMEDIATE
    )

    print(effect.generate_description())

    assert (
        effect.generate_description()
        == "Heal Self for 2 HP."
    )

    assert effect.duration == EffectDuration.IMMEDIATE


test_effect_description()