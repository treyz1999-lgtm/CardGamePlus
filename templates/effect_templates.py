
from enums.suit import Suit
from enums.effect_duration import EffectDuration
from enums.effect_type import EffectType
from enums.target import Target
from enums.trigger import Trigger
from enums.rank import Rank

def _generate_search_templates() -> dict:
    templates = {}
    """
    # Generates every supported SearchCriteria template.
    # These templates are reused by searchable Effects
    # instead of constructing SearchCriteria manually.
    Not every Effect template is used in V1.

    Additional templates are included so the game
    can expand without changing the template format.
    """
    # Rank only
    for rank in Rank:
        templates[rank.name.lower()] = (
            rank,
            None,
            None,
        )

    # Suit only
    for suit in Suit:
        templates[suit.name.lower()] = (
            None,
            suit,
            None,
        )

    # Rank + Suit
    for rank in Rank:
        for suit in Suit:
            templates[f"{rank.name.lower()}_{suit.name.lower()}"] = (
                rank,
                suit,
                None,
            )

    return templates


SEARCH_CRITERIA_TEMPLATES = _generate_search_templates()


EFFECT_TEMPLATES = {

    EffectType.HEAL: {

        "heal_1": {
            "cost": 50,
            "effect": {
                "effect_type": EffectType.HEAL,
                "trigger": Trigger.ON_PLAY,
                "target": Target.SELF,
                "value": 1,
                "duration": EffectDuration.IMMEDIATE,
                "condition": None,
                "search_criteria": None,
            },
        },

        "heal_2": {
            "cost": 100,
            "effect": {
                "effect_type": EffectType.HEAL,
                "trigger": Trigger.ON_PLAY,
                "target": Target.SELF,
                "value": 2,
                "duration": EffectDuration.IMMEDIATE,
                "condition": None,
                "search_criteria": None,
            },
        },

        "heal_3": {
            "cost": 200,
            "effect": {
                "effect_type": EffectType.HEAL,
                "trigger": Trigger.ON_PLAY,
                "target": Target.SELF,
                "value": 3,
                "duration": EffectDuration.IMMEDIATE,
                "condition": None,
                "search_criteria": None,
            },
        },
    },

    EffectType.DRAW_CARD: {

        "draw_1": {
            "cost": 100,
            "effect": {
                "effect_type": EffectType.DRAW_CARD,
                "trigger": Trigger.ON_PLAY,
                "target": Target.SELF,
                "value": 1,
                "duration": EffectDuration.IMMEDIATE,
                "condition": None,
                "search_criteria": None,
            },
        },

        "draw_2": {
            "cost": 225,
            "effect": {
                "effect_type": EffectType.DRAW_CARD,
                "trigger": Trigger.ON_PLAY,
                "target": Target.SELF,
                "value": 2,
                "duration": EffectDuration.IMMEDIATE,
                "condition": None,
                "search_criteria": None,
            },
        },

        "draw_3": {
            "cost": 450,
            "effect": {
                "effect_type": EffectType.DRAW_CARD,
                "trigger": Trigger.ON_PLAY,
                "target": Target.SELF,
                "value": 3,
                "duration": EffectDuration.IMMEDIATE,
                "condition": None,
                "search_criteria": None,
            },
        },
    },

    EffectType.RANK_UP: {

        "rank_up_1": {
            "cost": 50,
            "effect": {
                "effect_type": EffectType.RANK_UP,
                "trigger": Trigger.ON_PLAY,
                "target": Target.SELF,
                "value": 1,
                "duration": EffectDuration.IMMEDIATE,
                "condition": None,
                "search_criteria": None,
            },
        },

        "rank_up_2": {
            "cost": 100,
            "effect": {
                "effect_type": EffectType.RANK_UP,
                "trigger": Trigger.ON_PLAY,
                "target": Target.SELF,
                "value": 2,
                "duration": EffectDuration.IMMEDIATE,
                "condition": None,
                "search_criteria": None,
            },
        },

        "rank_up_5": {
            "cost": 300,
            "effect": {
                "effect_type": EffectType.RANK_UP,
                "trigger": Trigger.ON_PLAY,
                "target": Target.SELF,
                "value": 5,
                "duration": EffectDuration.IMMEDIATE,
                "condition": None,
                "search_criteria": None,
            },
        },

        "rank_up_10": {
            "cost": 800,
            "effect": {
                "effect_type": EffectType.RANK_UP,
                "trigger": Trigger.ON_PLAY,
                "target": Target.SELF,
                "value": 10,
                "duration": EffectDuration.IMMEDIATE,
                "condition": None,
                "search_criteria": None,
            },
        },
        "rank_up_100": {
            "cost": 8000,
            "effect": {
                "effect_type": EffectType.RANK_UP,
                "trigger": Trigger.ON_PLAY,
                "target": Target.SELF,
                "value": 100,
                "duration": EffectDuration.IMMEDIATE,
                "condition": None,
                "search_criteria": None,
            },
        },
    },


    EffectType.STUN: {

        "stun": {
            "cost": 500,
            "effect": {
                "effect_type": EffectType.STUN,
                "trigger": Trigger.ON_DEATH,
                "target": Target.OPPONENT,
                "value": 1,
                "duration": EffectDuration.IMMEDIATE,
                "condition": None,
                "search_criteria": None,
            },
        },
    },
}