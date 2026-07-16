from pydantic import BaseModel
from pydantic import Field


class CreateCardRequest(BaseModel):
    """
    Request to create a custom Card.
    """

    card_key: str = Field(
        min_length=2,
        max_length=2,
        description="Standard Card template identifier.",
        examples=["KH"],
    )

    effect_keys: list[str] = Field(
        default_factory=list,
        description="Owned Effect template identifiers to attach to the Card.",
        examples=[["heal_1", "rank_up_2"]],
    )


class CreateCardResponse(BaseModel):
    """
    Response returned after creating a custom Card.
    """

    card_id: int = Field(
        ge=1,
        description="Unique identifier for the newly created Card.",
        examples=[17],
    )

    message: str = Field(
        description="Confirmation that the Card was created successfully.",
        examples=["Card created successfully."],
    )


class CardResponse(BaseModel):
    """
    Persistent Card displayed in the User's collection.
    """

    card_id: int = Field(
        ge=1,
        description="Unique identifier for the Card.",
        examples=[17],
    )

    suit: str = Field(
        description="Card suit.",
        examples=["HEARTS"],
    )

    rank: int = Field(
        ge=2,
        le=14,
        description="Card rank (2-14 where 11 = Jack, 12 = Queen, 13 = King, and 14 = Ace).",
        examples=[13],
    )

    health: int = Field(
        ge=0,
        description="Current health value stored for the Card.",
        examples=[1],
    )

    effects: list[str] = Field(
        default_factory=list,
        description="Effect template keys attached to the Card.",
        examples=[["heal_1", "rank_up_2"]],
    )


class CardCollectionResponse(BaseModel):
    """
    Collection of Cards owned by the authenticated User.
    """

    cards: list[CardResponse] = Field(
        description="Every Card owned by the authenticated User.",
    )


class CardTemplateResponse(BaseModel):
    """
    Immutable standard Card template displayed when creating a Card.
    """

    card_key: str = Field(
        min_length=2,
        max_length=2,
        description="Standard Card template identifier.",
        examples=["KH"],
    )

    suit: str = Field(
        description="Card suit.",
        examples=["HEARTS"],
    )

    rank: int = Field(
        ge=2,
        le=14,
        description="Card rank (2-14 where 11 = Jack, 12 = Queen, 13 = King, and 14 = Ace).",
        examples=[13],
    )

    display_name: str = Field(
        description="User-facing standard Card name.",
        examples=["King of Hearts"],
    )


class CardTemplateCollectionResponse(BaseModel):
    """
    Available immutable standard Card templates.
    """

    templates: list[CardTemplateResponse] = Field(
        description="Every standard Card template available for custom Card creation.",
    )


class DeleteCardResponse(BaseModel):
    """
    Response returned after deleting a Card.
    """

    message: str = Field(
        description="Confirmation that the Card was deleted successfully.",
        examples=["Card deleted successfully."],
    )
