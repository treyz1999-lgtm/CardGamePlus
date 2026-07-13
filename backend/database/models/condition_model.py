
from sqlalchemy import Integer, ForeignKey
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database.base import Base

"""
Condition database table.

Stores the persistent information required to reconstruct
a runtime Condition object.

Each Condition belongs to exactly one Effect.

A Condition is optional for an Effect, but when one exists,
all Condition attributes are required.
"""

class ConditionModel(Base):

    __tablename__ = 'conditions'

    condition_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    effect_id: Mapped[int] = mapped_column(
        ForeignKey('effects.effect_id'),
        nullable=False,
    )

    attribute: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    comparison: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    value: Mapped[str] = mapped_column( #the value parameter for a Condition actually accepts any data type, but we will keep it as a string on the DB and the service can convert it to an int if needed depending on the comparison or attribute
        String,
        nullable=False,
    )

