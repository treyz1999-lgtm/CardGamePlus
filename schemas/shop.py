from pydantic import BaseModel
from pydantic import Field


class ShopInventoryItem(BaseModel):
    """
    A single purchasable Effect displayed in the Shop.
    """

    effect_key: str = Field(
        description="Unique identifier for the Effect template.",
        examples=["heal_1"],
    )

    name: str = Field(
        description="User-facing Effect name.",
        examples=["Heal 1"],
    )

    description: str = Field(
        description="User-facing description of the Effect behavior.",
        examples=["Heal Self for 1 HP."],
    )

    cost: int = Field(
        ge=0,
        description="Gold required to purchase the Effect.",
        examples=[50],
    )

    owned: bool = Field(
        description="Whether the authenticated User already owns this Effect.",
        examples=[False],
    )


class ShopInventoryResponse(BaseModel):
    """
    Complete Shop inventory returned to the frontend.
    """

    inventory: list[ShopInventoryItem]


class PurchaseEffectRequest(BaseModel):
    """
    Request to purchase an Effect template.
    """

    effect_key: str = Field(
        min_length=1,
        description="Unique identifier for the Effect template to purchase.",
        examples=["heal_2"],
    )


class PurchaseEffectResponse(BaseModel):
    """
    Response returned after purchasing an Effect.
    """

    message: str = Field(
        description="Purchase result.",
        examples=["Effect purchased successfully."],
    )

    gold: int = Field(
        ge=0,
        description="User's remaining gold after the purchase.",
        examples=[850],
    )
