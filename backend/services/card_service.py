from sqlalchemy.orm import Session

from database.models.card_model import CardModel

from enums.rank import Rank
from enums.suit import Suit

from models.card import Card
from models.effect import Effect

from services.effect_service import EffectService
from services.shop_services import ShopService

from templates.standard_deck import (
    STANDARD_DECK,
    create_standard_card,
)


class CardService:
    """
    Responsible for persisting and reconstructing Cards.

    Responsibilities
    ----------------
    - Create starter collections.
    - Create custom Cards.
    - Persist Card records.
    - Retrieve Cards owned by a User.
    - Retrieve an individual Card.
    - Delete Cards.
    - Reconstruct runtime Card objects.

    Effect persistence is delegated to the EffectService.
    Effect ownership is delegated to the ShopService.
    """

    def __init__(
        self,
        session: Session,
        effect_service: EffectService,
        shop_service: ShopService,
    ):
        self.session = session
        self.effect_service = effect_service
        self.shop_service = shop_service

    def create_starter_collection(
        self,
        user_id: int,
    ) -> None:
        """
        Create the standard starter collection for a new User.
        """

        existing_cards = (
            self.session.query(CardModel)
            .filter(
                CardModel.user_id == user_id
            )
            .count()
        )

        if existing_cards > 0:
            return

        for card_key in STANDARD_DECK:

            card = create_standard_card(card_key)

            self._create_card(
                user_id,
                card,
            )

    def create_custom_card(
        self,
        user_id: int,
        card_key: str,
        effect_keys: list[str],
    ) -> CardModel:
        """
        Create and persist a custom Card.

        A custom Card is constructed from one standard Card
        template and zero or more purchased Effect templates.
        """

        card = create_standard_card(card_key)

        for effect_key in effect_keys:

            if not self.shop_service.owns_effect(
                user_id,
                effect_key,
            ):
                raise ValueError(
                    f"User does not own '{effect_key}'."
                )

            template = self.shop_service.get_effect_template(
                effect_key,
            )

            if template is None:
                raise ValueError(
                    f"Unknown Effect '{effect_key}'."
                )

            effect_data = template["effect"]

            effect = Effect(
                effect_type=effect_data["effect_type"],
                trigger=effect_data["trigger"],
                target=effect_data["target"],
                value=effect_data["value"],
                duration=effect_data["duration"],
                condition=effect_data["condition"],
                search_criteria=effect_data["search_criteria"],
            )

            card.add_effect(effect)

        return self._create_card(
            user_id,
            card,
        )

    def _create_card(
        self,
        user_id: int,
        card: Card,
    ) -> CardModel:
        """
        Persist a Card and all attached Effects.
        """

        card_model = CardModel(
            user_id=user_id,
            suit=card.get_suit().name,
            rank=card.get_rank().value,
            health=card.get_health(),
        )

        self.session.add(card_model)
        self.session.commit()
        self.session.refresh(card_model)

        for effect in card.get_effects():
            self.effect_service.create_effect(
                card_model.card_id,
                effect,
            )

        return card_model

    def get_card(
        self,
        card_id: int,
    ) -> Card:
        """
        Retrieve a single runtime Card.
        """

        card_model = (
            self.session.query(CardModel)
            .filter(
                CardModel.card_id == card_id
            )
            .first()
        )

        if card_model is None:
            raise ValueError(
                "Card not found."
            )

        return self._build_card(card_model)

    def get_cards(
        self,
        user_id: int,
    ) -> list[Card]:
        """
        Retrieve every Card owned by a User.
        """

        card_models = (
            self.session.query(CardModel)
            .filter(
                CardModel.user_id == user_id
            )
            .all()
        )

        return [
            self._build_card(card_model)
            for card_model in card_models
        ]

    def delete_card(
        self,
        card_id: int,
    ) -> None:
        """
        Delete a Card.
        """

        card = (
            self.session.query(CardModel)
            .filter(
                CardModel.card_id == card_id
            )
            .first()
        )

        if card is None:
            raise ValueError(
                "Card not found."
            )

        self.session.delete(card)
        self.session.commit()

    def _build_card(
        self,
        card_model: CardModel,
    ) -> Card:
        """
        Reconstruct a runtime Card object.
        """

        effects = self.effect_service.get_effects(
            card_model.card_id
        )

        return Card(
            suit=Suit[card_model.suit],
            rank=Rank(card_model.rank),
            health=card_model.health,
            effects=effects,
        )