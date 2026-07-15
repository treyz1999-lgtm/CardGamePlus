from sqlalchemy.orm import Session

from database.models.card_model import CardModel

from enums.rank import Rank
from enums.suit import Suit

from models.card import Card

from services.effect_service import EffectService
from templates.standard_deck import STANDARD_DECK
from templates.standard_deck import create_standard_card


class CardService:
    """
    Responsible for persisting and reconstructing Cards.

    Responsibilities
    ----------------
    - Persist Card records.
    - Retrieve Cards owned by a User.
    - Retrieve an individual Card.
    - Delete Cards.
    - Reconstruct runtime Card objects.

    The CardService delegates all Effect persistence and
    reconstruction to the EffectService.
    """

    def __init__(
        self,
        session: Session,
        effect_service: EffectService,
    ):
        self.session = session
        self.effect_service = effect_service

    def create_card(
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
            raise ValueError("Card not found.")

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
            raise ValueError("Card not found.")

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

    def create_starter_collection(
            self,
            user_id: int,
    ) -> None:
        """
        Create the standard starter collection for a new User.

        Every standard card template is persisted once.
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

            self.create_card(
                user_id,
                card,
            )