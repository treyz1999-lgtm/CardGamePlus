from sqlalchemy.orm import Session

from database.models.deck_card_model import DeckCardModel
from database.models.deck_model import DeckModel

from models.deck import Deck

from services.card_service import CardService


class DeckService:
    """
    Responsible for persisting and reconstructing Decks.

    Responsibilities
    ----------------
    - Persist Deck records.
    - Retrieve Decks owned by a User.
    - Add Cards to Decks.
    - Remove Cards from Decks.
    - Delete Decks.
    - Reconstruct runtime Deck objects.

    The DeckService delegates Card reconstruction to the
    CardService.
    """

    def __init__(
        self,
        session: Session,
        card_service: CardService,
    ):
        self.session = session
        self.card_service = card_service

    def create_deck(
        self,
        user_id: int,
        name: str,
        card_ids: list[int],
    ) -> DeckModel:
        """
        Persist a Deck and its Card relationships.
        """

        deck_model = DeckModel(
            user_id=user_id,
            name=name,
        )

        self.session.add(deck_model)
        self.session.commit()
        self.session.refresh(deck_model)

        for card_id in card_ids:

            deck_card = DeckCardModel(
                deck_id=deck_model.deck_id,
                card_id=card_id,
            )

            self.session.add(deck_card)

        self.session.commit()

        return deck_model

    def get_deck(
        self,
        deck_id: int,
    ) -> Deck:
        """
        Retrieve a runtime Deck.
        """

        deck_model = (
            self.session.query(DeckModel)
            .filter(
                DeckModel.deck_id == deck_id
            )
            .first()
        )

        if deck_model is None:
            raise ValueError("Deck not found.")

        return self._build_deck(deck_model)

    def get_decks(
            self,
            user_id: int,
    ) -> list[dict]:
        """
        Retrieve every Deck owned by a User together with
        the information required by the deck builder.
        """

        deck_models = (
            self.session.query(DeckModel)
            .filter(
                DeckModel.user_id == user_id,
            )
            .all()
        )

        return [
            {
                "deck_id": deck.deck_id,
                "name": deck.name,
            }
            for deck in deck_models
        ]

    def add_card_to_deck(
        self,
        deck_id: int,
        card_id: int,
    ) -> None:
        """
        Add a Card to a Deck.
        """

        deck_card = DeckCardModel(
            deck_id=deck_id,
            card_id=card_id,
        )

        self.session.add(deck_card)
        self.session.commit()

    def remove_card_from_deck(
        self,
        deck_id: int,
        card_id: int,
    ) -> None:
        """
        Remove a Card from a Deck.
        """

        deck_card = (
            self.session.query(DeckCardModel)
            .filter(
                DeckCardModel.deck_id == deck_id,
                DeckCardModel.card_id == card_id,
            )
            .first()
        )

        if deck_card is None:
            raise ValueError("Card is not in the deck.")

        self.session.delete(deck_card)
        self.session.commit()

    def delete_deck(
        self,
        deck_id: int,
    ) -> None:
        """
        Delete a Deck.
        """

        deck = (
            self.session.query(DeckModel)
            .filter(
                DeckModel.deck_id == deck_id
            )
            .first()
        )

        if deck is None:
            raise ValueError("Deck not found.")

        self.session.delete(deck)
        self.session.commit()

    def _build_deck(
        self,
        deck_model: DeckModel,
    ) -> Deck:
        """
        Reconstruct a runtime Deck object.
        """

        deck_cards = (
            self.session.query(DeckCardModel)
            .filter(
                DeckCardModel.deck_id == deck_model.deck_id
            )
            .all()
        )

        cards = [
            self.card_service.get_card(deck_card.card_id)
            for deck_card in deck_cards
        ]

        return Deck(
            cards=cards,
            name=deck_model.name,
        )

    def get_deck_details(
            self,
            user_id: int,
            deck_id: int,
    ) -> dict:
        """
        Retrieve a Deck together with the information
        required by the deck builder.
        """

        deck_model = (
            self.session.query(DeckModel)
            .filter(
                DeckModel.deck_id == deck_id,
                DeckModel.user_id == user_id,
            )
            .first()
        )

        if deck_model is None:
            raise ValueError(
                "Deck not found."
            )

        deck_cards = (
            self.session.query(DeckCardModel)
            .filter(
                DeckCardModel.deck_id == deck_id,
            )
            .all()
        )

        collection = {
            card["card_id"]: card
            for card in self.card_service.get_card_collection(
                user_id,
            )
        }

        return {
            "deck_id": deck_model.deck_id,
            "name": deck_model.name,
            "cards": [
                collection[deck_card.card_id]
                for deck_card in deck_cards
                if deck_card.card_id in collection
            ],
        }