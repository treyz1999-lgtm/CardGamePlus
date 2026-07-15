from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from database.database import get_db
from database.models.user_model import UserModel

from dependencies.auth import get_current_user

from schemas.deck import (
    CreateDeckRequest,
    CreateDeckResponse,
    DeckResponse,
    DeckCollectionResponse,
    DeckDetailsResponse,
    AddCardRequest,
    AddCardResponse,
    RemoveCardResponse,
    DeleteDeckResponse,
)

from services.user_service import UserService
from services.shop_services import ShopService
from services.effect_service import EffectService
from services.card_service import CardService
from services.deck_service import DeckService


router = APIRouter(
    prefix="/decks",
    tags=["Decks"],
)


def get_deck_service(
    session: Session,
) -> DeckService:
    """
    Construct a DeckService and its dependencies.
    """

    user_service = UserService(session)

    shop_service = ShopService(
        session,
        user_service,
    )

    effect_service = EffectService(session)

    card_service = CardService(
        session,
        effect_service,
        shop_service,
    )

    return DeckService(
        session,
        card_service,
    )


@router.post(
    "/",
    response_model=CreateDeckResponse,
)
def create_deck(
    request: CreateDeckRequest,
    current_user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> CreateDeckResponse:
    """
    Create a new Deck.
    """

    deck_service = get_deck_service(session)

    deck_model = deck_service.create_deck(
        current_user.user_id,
        request.name,
        request.card_ids,
    )

    return CreateDeckResponse(
        deck_id=deck_model.deck_id,
        message="Deck created successfully.",
    )


@router.get(
    "/",
    response_model=DeckCollectionResponse,
)
def get_decks(
    current_user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> DeckCollectionResponse:
    """
    Retrieve every Deck owned by the authenticated User.
    """

    deck_service = get_deck_service(session)

    decks = deck_service.get_decks(
        current_user.user_id,
    )

    return DeckCollectionResponse(
        decks=[
            DeckResponse(**deck)
            for deck in decks
        ],
    )


@router.get(
    "/{deck_id}",
    response_model=DeckDetailsResponse,
)
def get_deck(
    deck_id: int,
    current_user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> DeckDetailsResponse:
    """
    Retrieve a Deck and its Cards.
    """

    deck_service = get_deck_service(session)

    deck = deck_service.get_deck_details(
        current_user.user_id,
        deck_id,
    )

    return DeckDetailsResponse(
        **deck,
    )


@router.post(
    "/{deck_id}/cards",
    response_model=AddCardResponse,
)
def add_card_to_deck(
    deck_id: int,
    request: AddCardRequest,
    current_user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> AddCardResponse:
    """
    Add a Card to a Deck.
    """

    deck_service = get_deck_service(session)

    deck_service.add_card_to_deck(
        current_user.user_id,
        deck_id,
        request.card_id,
    )

    return AddCardResponse(
        message="Card added to Deck successfully.",
    )


@router.delete(
    "/{deck_id}/cards/{card_id}",
    response_model=RemoveCardResponse,
)
def remove_card_from_deck(
    deck_id: int,
    card_id: int,
    current_user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> RemoveCardResponse:
    """
    Remove a Card from a Deck.
    """

    deck_service = get_deck_service(session)

    deck_service.remove_card_from_deck(
        current_user.user_id,
        deck_id,
        card_id,
    )

    return RemoveCardResponse(
        message="Card removed from Deck successfully.",
    )


@router.delete(
    "/{deck_id}",
    response_model=DeleteDeckResponse,
)
def delete_deck(
    deck_id: int,
    current_user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> DeleteDeckResponse:
    """
    Delete a Deck.
    """

    deck_service = get_deck_service(session)

    deck_service.delete_deck(
        current_user.user_id,
        deck_id,
    )

    return DeleteDeckResponse(
        message="Deck deleted successfully.",
    )