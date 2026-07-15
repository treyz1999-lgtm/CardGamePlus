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
from templates.effect_templates import EFFECT_TEMPLATES


class ShopService:

    def __init__(
        self,
        session: Session,
        user_service: UserService,
    ):
        self.session = session
        self.user_service = user_service

        self._inventory = {}

        for effect_group in EFFECT_TEMPLATES.values():
            self._inventory.update(effect_group)

    def get_shop_inventory(self) -> dict[str, dict]:
        """
        Retrieve every purchasable Effect template.
        """

        return self._inventory

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
    ) -> OwnedEffectModel:
        """
        Purchase an Effect template.
        """

        template = self._inventory.get(effect_key)

        if template is None:
            raise ValueError("Unknown effect.")

        if self.owns_effect(
            user_id,
            effect_key,
        ):
            raise ValueError("Effect already owned.")

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
        self.session.refresh(owned)

        return owned

    def owns_effect(
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

        self.user_service.update_gold(
            user_id,
            amount,
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
            raise ValueError("Insufficient gold.")

        self.user_service.update_gold(
            user_id,
            -amount,
        )

        def get_effect_template(
                self,
                user_id: int,
                effect_key: str,
        ) -> dict:
            """
            Retrieve an owned Effect template.

            The User must already own the Effect before it can
            be attached to a custom Card.
            """

            if not self.owns_effect(
                    user_id,
                    effect_key,
            ):
                raise ValueError(
                    "User does not own this Effect."
                )

            template = self._inventory.get(effect_key)

            if template is None:
                raise ValueError(
                    "Unknown Effect."
                )

            return template