from models.condition import Condition
from enums import ConditionAttribute, Comparison


def test_condition_text():

    condition = Condition(
        ConditionAttribute.BASE_RANK,
        Comparison.LESS_THAN,
        3
    )

    print(condition.generate_text())

    assert condition.generate_text() == "If Base Rank is less than 3"


test_condition_text()