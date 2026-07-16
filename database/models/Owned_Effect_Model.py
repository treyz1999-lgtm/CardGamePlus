from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from database.base import Base
from sqlalchemy import UniqueConstraint

class OwnedEffectModel(Base):
    """
    UserEffect database table.

    Stores which Effect templates a User has permanently
    unlocked through the Shop.

    Each record references an Effect template using its
    unique template key (for example, "rank_up_1" or
    "heal_2").

    The template definitions themselves are stored in
    effects_template.py.

    This table does not store Effect data directly.

    Instead, the effect_key references a template defined in
    effects_template.py, allowing the application to reconstruct
    the corresponding Effect whenever needed.
    """

    __tablename__ = "user_effects"

    user_effect_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id"),
        nullable=False,
    )

    effect_key: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "effect_key",
            name="uq_user_effect",
        ),
    )

    def __init__(
            self,
            user_id: int,
            effect_key: str,
    ):
        """
        Initialize an owned Effect record.

        The database generates the primary key.
        """

        self.user_id = user_id
        self.effect_key = effect_key