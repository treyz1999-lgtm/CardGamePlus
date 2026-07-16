
from sqlalchemy import Integer, ForeignKey
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database.base import Base

class SearchCriteriaModel(Base):

    __tablename__ = 'search_criteria'

    search_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    effect_id: Mapped[int] = mapped_column(
        ForeignKey('effects.effect_id'),
        nullable=False,
    )

    rank: Mapped[int] = mapped_column( #all params are optional for SearchCriteria; Rank enum
        Integer,
        nullable= True
    )

    suit: Mapped[str] = mapped_column(  # all params are optional for SearchCriteria; Suit Enum
        String,
        nullable=True
    )

    effect_type: Mapped[str] = mapped_column( # all params are optional for SearchCriteria; EffectType Enum
        String,
        nullable=True
    )

    def __init__(
            self,
            effect_id: int,
            rank: int | None = None,
            suit: str | None = None,
            effect_type: str | None = None,
    ):
        """
        Initialize a SearchCriteria database record.

        All search criteria are optional. Any attribute left as
        None is ignored when reconstructing the runtime
        SearchCriteria object.
        """

        self.effect_id = effect_id
        self.rank = rank
        self.suit = suit
        self.effect_type = effect_type