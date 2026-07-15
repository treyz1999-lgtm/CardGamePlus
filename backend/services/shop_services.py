"""
Shop Service

Responsible for managing the in-game economy.

Responsibilities
----------------
- Retrieve the shop inventory.
- Retrieve Effects owned by a User.
- Purchase new Effect templates.
- Award gold.
- Spend gold.
- Check Effect ownership.

The ShopService does not create Cards.

Card creation is delegated to the CardService.
"""
from sqlalchemy.orm import Session

from database.models.Owned_Effect_Model import OwnedEffectModel
from services.user_service import UserService


class ShopService:

    def __init__(
        self,
        session: Session,
        user_service: UserService,
    ):
        self.session = session
        self.user_service = user_service

    def get_shop_inventory(self):
        pass

    def get_owned_effects(
            self,
            user_id: int,
    ) -> list[OwnedEffectModel]:
        """
        Retrieve every unlocked Effect owned by a User.
        """

        return (
            self.session.query(OwnedEffectModel)
            .filter(
                OwnedEffectModel.user_id == user_id
            )
            .all()
        )

    def purchase_effect(
            self,
            user_id: int,
            effect_key: str,
    ):
        """
        Purchase an Effect template.
        """

        template = self.inventory.get(effect_key)

        if template is None:
            raise ValueError("Unknown effect.")

        if self.user_owns_effect(
                user_id,
                effect_key,
        ):
            raise ValueError(
                "Effect already owned."
            )

        cost = template["cost"]

        self.spend_gold(
            user_id,
            cost,
        )

        owned = OwnedEffectModel(
            user_id=user_id,
            effect_key=effect_key,
        )

        self.session.add(owned)
        self.session.commit()

        return owned

    def user_owns_effect(
            self,
            user_id: int,
            effect_key: str,
    ) -> bool:
        """
        Determine whether a User owns an unlocked Effect.
        """

        owned_effect = (
            self.session.query(OwnedEffectModel)
            .filter(
                OwnedEffectModel.user_id == user_id,
                OwnedEffectModel.effect_key == effect_key,
            )
            .first()
        )

        return owned_effect is not None

    def add_gold(
            self,
            user_id: int,
            amount: int,
    ) -> None:
        """
        Award gold to a User.
        """

        user = self.user_service.get_by_id(user_id)

        self.user_service.update_gold(
            user_id,
            user.gold + amount,
        )

    def spend_gold(
            self,
            user_id: int,
            amount: int,
    ) -> None:
        """
        Spend a User's gold.
        """

        user = self.user_service.get_by_id(user_id)

        if user.gold < amount:
            raise ValueError(
                "Insufficient gold."
            )

        self.user_service.update_gold(
            user_id,
            user.gold - amount,
        )