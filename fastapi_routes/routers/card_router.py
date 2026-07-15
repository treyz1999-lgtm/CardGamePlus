from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from database.database import get_db
from database.models.user_model import UserModel

from dependencies.auth import get_current_user

from schemas.card import (
    CreateCardRequest,
    CreateCardResponse,
    CardResponse,
    CardCollectionResponse,
    DeleteCardResponse,
)

from services.user_service import UserService
from services.shop_services import ShopService
from services.effect_service import EffectService
from services.card_service import CardService


router = APIRouter(
    prefix="/cards",
    tags=["Cards"],
)


def get_card_service(
    session: Session,
) -> CardService:
    """
    Construct a CardService and its dependencies.
    """

    user_service = UserService(session)

    shop_service = ShopService(
        session,
        user_service,
    )

    effect_service = EffectService(session)

    return CardService(
        session,
        effect_service,
        shop_service,
    )


@router.post(
    "/",
    response_model=CreateCardResponse,
)
def create_card(
    request: CreateCardRequest,
    current_user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> CreateCardResponse:
    """
    Create a new custom Card.
    """

    card_service = get_card_service(session)

    card_model = card_service.create_custom_card(
        current_user.user_id,
        request.card_key,
        request.effect_keys,
    )

    return CreateCardResponse(
        card_id=card_model.card_id,
        message="Card created successfully.",
    )


@router.get(
    "/",
    response_model=CardCollectionResponse,
)
def get_cards(
    current_user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> CardCollectionResponse:
    """
    Retrieve every Card owned by the authenticated User.
    """

    card_service = get_card_service(session)

    collection = card_service.get_card_collection(
        current_user.user_id,
    )

    return CardCollectionResponse(
        cards=[
            CardResponse(**card)
            for card in collection
        ],
    )


@router.delete(
    "/{card_id}",
    response_model=DeleteCardResponse,
)
def delete_card(
    card_id: int,
    current_user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> DeleteCardResponse:
    """
    Delete a custom Card.
    """

    card_service = get_card_service(session)

    card_service.delete_card(
        card_id,
    )

    return DeleteCardResponse(
        message="Card deleted successfully.",
    )