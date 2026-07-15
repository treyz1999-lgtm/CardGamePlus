from sqlalchemy import Integer, ForeignKey
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database.base import Base
from enums.effect_duration import EffectDuration


class EffectModel(Base):
    """
       What information is required to reconstruct an Effect object?
       - An EffectType Object which is an enum
       - A Trigger Object which is an enum
       - A Target Object which is an enum
       - A value which is an integer
       - An EffectDuration Object which is an enum
       - An optional Condition Object - will be its own table that references this table's effect_id
       -An optional SearchCriteria Object - will be its own table that references this table's effect_id

       Persistent Attributes
        ---------------------
        - effect_type
        - trigger
        - target
        - duration
        - value

        These values are stored permanently in the database so that
        the service can reconstruct a runtime Effect object whenever
        one is requested.

       Which table owns each relationship?
       Each Effect belongs to exactly one Card, but the Condition will actually hav to be its own table that has an Effect_ID to relate each condition to its effect here on this table. Same with the SearchCriteria as well, both of these can be nullable
       """

    __tablename__ = "effects"

    effect_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    card_id: Mapped[int] = mapped_column(
        ForeignKey('cards.card_id'),
        nullable=False,
    )

    effect_type: Mapped[str] = mapped_column( #this will hold the Enum name like RANK_UP and can not be null on the DB
        String,
        nullable=False,
    )

    trigger: Mapped[str] = mapped_column(  # this will hold the Enum name like ON_PLAY and can not be null on the DB
        String,
        nullable=False,
    )

    target: Mapped[str] = mapped_column(  # this will hold the Enum name like ON_PLAY and can not be null on the DB
        String,
        nullable=False,
    )

    value: Mapped[int] = mapped_column( #this can't be null so we will just default to 0 if nothing is passed in
        Integer,
        nullable = False,
        default=0,
    )

    duration: Mapped[str] = mapped_column( # this will hold the Enum name like IMMEDIATE and can not be null on the DB, all effect_durations default to immediate anyway so we can just make that the default on the DB as well
        String,
        nullable = False,
        default= EffectDuration.IMMEDIATE.name
    )

    def __init__(
            self,
            card_id: int,
            effect_type: str,
            trigger: str,
            target: str,
            value: int = 0,
            duration: str = EffectDuration.IMMEDIATE.name,
    ):
        self.card_id = card_id
        self.effect_type = effect_type
        self.trigger = trigger
        self.target = target
        self.value = value
        self.duration = duration