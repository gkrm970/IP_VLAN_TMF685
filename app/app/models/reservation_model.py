import uuid
from typing import Any
from urllib.parse import urljoin

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import models, schemas, settings
from app.db.base import Base

_ALL_DELETE_ORPHAN = "all, delete-orphan"

class Reservation(Base):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    href: Mapped[str] = mapped_column(String(255))
    type: Mapped[str | None] = mapped_column(String(255))
    reservation_state: Mapped[str] = mapped_column(String(255))

    related_parties: Mapped[models.ReservationRelatedParty] = relationship(
        back_populates="reservation", lazy="selectin", cascade=_ALL_DELETE_ORPHAN, uselist=False
    )
    reservation_item: Mapped[list[models.ReservationItem]] = relationship(
        back_populates="reservation", lazy="selectin", cascade=_ALL_DELETE_ORPHAN
    )
    valid_for: Mapped[models.ValidFor] = relationship(
        back_populates="reservation", lazy="selectin", cascade=_ALL_DELETE_ORPHAN, uselist=False
    )

    @classmethod
    def from_schema(cls, schema: schemas.ReservationCreate) -> "Reservation":
        reservation_id = str(uuid.uuid4())

        related_parties = models.ReservationRelatedParty.from_schema(schema.related_parties)
        print(f'{related_parties=}')
        reservation_item_list = [
            models.ReservationItem.from_schema(reservation_item)
            for reservation_item in schema.reservation_item
        ]
        print(f'{reservation_item_list=}')
        valid_for = models.ValidFor.from_schema(schema.valid_for)
        print(f'{valid_for=}')

        return cls(
            id=reservation_id,
            href=f"resource/{reservation_id}",
            type=schema.type,
            reservation_state=schema.reservation_state,
            related_parties=related_parties,
            reservation_item=reservation_item_list,
            valid_for=valid_for
        )

    def to_schema(self) -> dict[str, Any]:
        data = schemas.Reservation.model_validate(self).model_dump(by_alias=True)
        # data = schemas.Reservation.model_validate(self).model_dump(
        #     by_alias=True, include=include
        # )

        data["href"] = urljoin(
            f"{urljoin(str(settings.API_BASE_URL), settings.API_PREFIX)}/",
            self.href,
        )

        return data
