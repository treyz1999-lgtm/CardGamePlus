from pydantic import BaseModel
from pydantic import Field

from schemas.card import CardResponse


class CreateDeckRequest(BaseModel):
    """
    Request to create a new Deck.
    """

    name: str = Field(
        min_length=1,
        max_length=50,
        description="Name of the Deck.",
        examples=["Aggro Deck"],
    )

    card_ids: list[int] = Field(
        default_factory=list,
        description="Card identifiers to include in the Deck.",
        examples=[[17, 18, 19, 20]],
    )


class CreateDeckResponse(BaseModel):
    """
    Response returned after creating a Deck.
    """

    deck_id: int = Field(
        ge=1,
        description="Unique identifier for the newly created Deck.",
        examples=[3],
    )

    message: str = Field(
        description="Confirmation that the Deck was created successfully.",
        examples=["Deck created successfully."],
    )


class DeckResponse(BaseModel):
    """
    Persistent Deck displayed in the Deck Builder.
    """

    deck_id: int = Field(
        ge=1,
        description="Unique identifier for the Deck.",
        examples=[3],
    )

    name: str = Field(
        description="Name of the Deck.",
        examples=["Aggro Deck"],
    )


class DeckCollectionResponse(BaseModel):
    """
    Collection of Decks owned by the authenticated User.
    """

    decks: list[DeckResponse] = Field(
        description="Every Deck owned by the authenticated User.",
    )


class DeckDetailsResponse(BaseModel):
    """
    Persistent Deck displayed in the Deck Builder.
    """

    deck_id: int = Field(
        ge=1,
        description="Unique identifier for the Deck.",
        examples=[3],
    )

    name: str = Field(
        description="Name of the Deck.",
        examples=["Aggro Deck"],
    )

    cards: list[CardResponse] = Field(
        default_factory=list,
        description="Cards currently assigned to the Deck.",
    )


class AddCardRequest(BaseModel):
    """
    Request to add a Card to a Deck.
    """

    card_id: int = Field(
        ge=1,
        description="Unique identifier for the Card to add to the Deck.",
        examples=[17],
    )


class AddCardResponse(BaseModel):
    """
    Response returned after adding a Card to a Deck.
    """

    message: str = Field(
        description="Confirmation that the Card was added to the Deck successfully.",
        examples=["Card added to Deck successfully."],
    )


class RemoveCardResponse(BaseModel):
    """
    Response returned after removing a Card from a Deck.
    """

    message: str = Field(
        description="Confirmation that the Card was removed from the Deck successfully.",
        examples=["Card removed from Deck successfully."],
    )


class DeleteDeckResponse(BaseModel):
    """
    Response returned after deleting a Deck.
    """

    message: str = Field(
        description="Confirmation that the Deck was deleted successfully.",
        examples=["Deck deleted successfully."],
    )