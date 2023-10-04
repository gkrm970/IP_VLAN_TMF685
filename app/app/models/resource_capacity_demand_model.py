import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import Annotated

from app import models
from app.db.base import Base

datetime = Annotated[DateTime, datetime.datetime]


class ResourceCapacityDemand(Base):
    __tablename__ = 'resource_capacity_demand'

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    baseType: Mapped[str] = mapped_column(String(255))
    schemaLocation: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255))
    capacityDemandAmount: Mapped[str] = mapped_column(String(255))

    # 1..1 relationship with ReservationItem table and ResourceCapacityDemand table (ResourceCapacityDemand table is
    # child)
    reservation_item_id: Mapped[str] = mapped_column(String), ForeignKey("reservation_item.id")
    reservation_item = relationship("ReservationItem", back_populates="resource_capacity_demand")  # 1..1

    # 1..0..1 relationship with ResourceCapacityDemand table and PlaceRef table (ResourceCapacityDemand table is parent)
    place_ref = relationship("PlaceRef", back_populates="resource_capacity_demand")

    # 1..0..1 relationship with ResourceCapacityDemand table and ApplicationTimePeriod table (ResourceCapacityDemand
    # table is parent)
    applicable_time_period = relationship("ApplicableTimePeriod", back_populates="resource_capacity_demand")
    #
    # 1..1 relationship with ResourceCapacityDemand table and ResourcePoolRef table (ResourceCapacityDemand table is
    # parent)
    resource_pool_ref = relationship("ResourcePoolRef", back_populates="resource_capacity_demand")  # 1..1
