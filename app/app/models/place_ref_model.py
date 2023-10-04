import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import Annotated

from app import models
from app.db.base import Base

datetime = Annotated[DateTime, datetime.datetime]


class PlaceRef(Base):
    __tablename__ = 'place_ref'

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    href: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    referredType: Mapped[str] = mapped_column(String(255))

    # 1..0..1 relationship with ResourceCapacityDemand table and PlaceRef table (PlaceRef table is child)
    resource_capacity_demand_id: Mapped[str] = mapped_column(String), ForeignKey("resource_capacity_demand.id")
    resource_capacity_demand = relationship("ResourceCapacityDemand", back_populates="place_ref")  # 1..0..1

