from sqlalchemy.orm import Session

from database.models.condition_model import ConditionModel
from database.models.effect_model import EffectModel
from database.models.search_model import SearchCriteriaModel

from enums.condition import ConditionAttribute, Comparison
from enums.effect_duration import EffectDuration
from enums.effect_type import EffectType
from enums.rank import Rank
from enums.suit import Suit
from enums.target import Target
from enums.trigger import Trigger

from models.condition import Condition
from models.effect import Effect
from models.search_criteria import SearchCriteria


class EffectService:
    """
    Responsible for persisting and reconstructing Effects.

    Responsibilities
    ----------------
    - Persist Effect records.
    - Persist optional Condition records.
    - Persist optional SearchCriteria records.
    - Retrieve Effects belonging to a Card.
    - Reconstruct runtime Effect objects.
    """

    def __init__(self, session: Session):
        self.session = session

    def create_effect(
        self,
        card_id: int,
        effect_key: str,
        effect: Effect,
    ) -> EffectModel:
        """
        Persist an Effect attached to a Card.
        """

        effect_model = EffectModel(
            card_id=card_id,
            effect_key=effect_key,
            effect_type=effect.effect_type.name,
            trigger=effect.trigger.name,
            target=effect.target.name,
            value=effect.value,
            duration=effect.duration.name,
        )

        self.session.add(effect_model)
        self.session.commit()
        self.session.refresh(effect_model)

        if effect.condition is not None:

            condition_model = ConditionModel(
                effect_id=effect_model.effect_id,
                attribute=effect.condition.attribute.name,
                comparison=effect.condition.comparison.name,
                value=str(effect.condition.value),
            )

            self.session.add(condition_model)

        if effect.search_criteria is not None:

            search_model = SearchCriteriaModel(
                effect_id=effect_model.effect_id,
                rank=(
                    effect.search_criteria.rank.value
                    if effect.search_criteria.rank
                    else None
                ),
                suit=(
                    effect.search_criteria.suit.name
                    if effect.search_criteria.suit
                    else None
                ),
                effect_type=(
                    effect.search_criteria.effect.name
                    if effect.search_criteria.effect
                    else None
                ),
            )

            self.session.add(search_model)

        self.session.commit()

        return effect_model

    def get_effects(
        self,
        card_id: int,
    ) -> list[Effect]:
        """
        Retrieve every Effect attached to a Card.
        """

        effect_models = (
            self.session.query(EffectModel)
            .filter(
                EffectModel.card_id == card_id
            )
            .all()
        )

        return [
            self._build_effect(effect_model)
            for effect_model in effect_models
        ]

    def delete_effect(
        self,
        effect_id: int,
    ) -> None:
        """
        Delete an Effect.
        """

        effect = (
            self.session.query(EffectModel)
            .filter(
                EffectModel.effect_id == effect_id
            )
            .first()
        )

        if effect is None:
            raise ValueError(
                "Effect not found."
            )

        self.session.delete(effect)
        self.session.commit()

    def _build_effect(
        self,
        effect_model: EffectModel,
    ) -> Effect:
        """
        Reconstruct a runtime Effect object.
        """

        effect = Effect(
            effect_type=EffectType[effect_model.effect_type],
            trigger=Trigger[effect_model.trigger],
            target=Target[effect_model.target],
            duration=EffectDuration[effect_model.duration],
            value=effect_model.value,
            condition=self._build_condition(effect_model),
            search_criteria=self._build_search_criteria(effect_model),
        )

        effect.effect_key = effect_model.effect_key

        return effect
    def _build_condition(
        self,
        effect_model: EffectModel,
    ) -> Condition | None:
        """
        Reconstruct the optional Condition attached to an Effect.
        """

        condition_model = (
            self.session.query(ConditionModel)
            .filter(
                ConditionModel.effect_id == effect_model.effect_id
            )
            .first()
        )

        if condition_model is None:
            return None

        attribute = ConditionAttribute[
            condition_model.attribute
        ]

        value = condition_model.value

        if attribute in {
            ConditionAttribute.BASE_RANK,
            ConditionAttribute.HEALTH,
            ConditionAttribute.HAND_SIZE,
            ConditionAttribute.PLAYER_HP,
            ConditionAttribute.OPPONENT_HP,
        }:
            value = int(value)

        return Condition(
            attribute=attribute,
            comparison=Comparison[
                condition_model.comparison
            ],
            value=value,
        )

    def _build_search_criteria(
        self,
        effect_model: EffectModel,
    ) -> SearchCriteria | None:
        """
        Reconstruct the optional SearchCriteria attached to an Effect.
        """

        search_model = (
            self.session.query(SearchCriteriaModel)
            .filter(
                SearchCriteriaModel.effect_id == effect_model.effect_id
            )
            .first()
        )

        if search_model is None:
            return None

        return SearchCriteria(
            rank=(
                Rank(search_model.rank)
                if search_model.rank is not None
                else None
            ),
            suit=(
                Suit[search_model.suit]
                if search_model.suit is not None
                else None
            ),
            effect=(
                EffectType[search_model.effect_type]
                if search_model.effect_type is not None
                else None
            ),
        )

    def get_effect_models(
        self,
        card_id: int,
    ) -> list[EffectModel]:
        """
        Retrieve every persistent Effect attached to a Card.

        This method is used by application features
        (such as the collection screen) that need the
        persisted Effect records rather than reconstructed
        runtime Effect objects.
        """

        return (
            self.session.query(EffectModel)
            .filter(
                EffectModel.card_id == card_id,
            )
            .all()
        )
