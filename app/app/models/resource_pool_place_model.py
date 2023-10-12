from typing import TYPE_CHECKING, Optional
from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base
from app import schemas

if TYPE_CHECKING:
    from app.models import Capacity


class ResourcePlace(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True
                                    )
    name: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255))

    capacity_id: Mapped[str] = mapped_column(ForeignKey("capacity.id"))
    capacity: Mapped["Capacity"] = relationship(back_populates="place")

    # capacity: Mapped["Capacity"] = relationship(
    #     back_populates="place", uselist=False)

    @classmethod
    def from_schema(cls, schema: schemas.ResourcePlace) -> "ResourcePlace":
        print(f'schema:{schema}')
        # related_party = schemas.ResourceRelatedParty(id=s,)

        return cls(**schema.model_dump())