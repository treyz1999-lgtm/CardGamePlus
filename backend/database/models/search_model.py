
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