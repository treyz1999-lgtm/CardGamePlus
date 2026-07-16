from enums import EffectDuration
from models.effect import Effect
from models.condition import Condition
from enums import EffectType
from enums import Trigger
from enums import Target
from enums import ConditionAttribute, Comparison


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