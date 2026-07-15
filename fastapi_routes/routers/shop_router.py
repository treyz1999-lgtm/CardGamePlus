from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from database.database import get_db
from database.models.user_model import UserModel

from dependencies.auth import get_current_user

from schemas.shop import (
    ShopInventoryItem,
    ShopInventoryResponse,
    PurchaseEffectRequest,
    PurchaseEffectResponse,
)

from services.user_service import UserService
from services.shop_services import ShopService


router = APIRouter(
    prefix="/shop",
    tags=["Shop"],
)


@router.get(
    "",
    response_model=ShopInventoryResponse,
)
def get_shop_inventory(
    current_user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> ShopInventoryResponse:
    """
    Retrieve the Shop inventory for the authenticated User.
    """

    user_service = UserService(session)

    shop_service = ShopService(
        session,
        user_service,
    )

    inventory = shop_service.get_shop_inventory(
        current_user.user_id,
    )

    return ShopInventoryResponse(
        inventory=[
            ShopInventoryItem(**item)
            for item in inventory
        ],
    )


@router.post(
    "/purchase",
    response_model=PurchaseEffectResponse,
)
def purchase_effect(
    request: PurchaseEffectRequest,
    current_user: UserModel = Depends(get_current_user),
    session: Session = Depends(get_db),
) -> PurchaseEffectResponse:
    """
    Purchase an Effect template.
    """

    user_service = UserService(session)

    shop_service = ShopService(
        session,
        user_service,
    )

    shop_service.purchase_effect(
        current_user.user_id,
        request.effect_key,
    )

    user = user_service.get_by_id(
        current_user.user_id,
    )

    return PurchaseEffectResponse(
        message="Effect purchased successfully.",
        gold=user.gold,
    )