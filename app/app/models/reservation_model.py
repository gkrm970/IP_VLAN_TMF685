import datetime
from typing_extensions import Annotated
from sqlalchemy import ForeignKey, DateTime, String

from sqlalchemy import String, ForeignKey, Column, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

datetime = Annotated[DateTime, datetime.datetime]


class Reservation(Base):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    baseType: Mapped[str] = mapped_column(String(255))
    schemaLocation: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255))
    href: Mapped[str] = mapped_column(String(255))
    reservationItem: Mapped[str] = mapped_column(String(255))
    valid_for: Mapped[str] = mapped_column(String(255))
    relatedParty: Mapped[str | None] = mapped_column(String(255))

    # 1..1 relationship with Reservation table and RelatedPartyRef table (Reservation table is parent)
    related_party_ref = relationship("RelatedPartyRef", back_populates="reservation", uselist=False)  # 1..1

    # 1..1 relationship with Reservation table and ProductOfferingRef table (Reservation table is parent)
    product_offering_ref = relationship("ProductOfferingRef", back_populates="reservation", uselist=False)  # 1..1

    # 1..0..1 relationship with Reservation table and RequestedPeriod table (Reservation table is parent)
    requested_period = relationship("RequestedPeriod", back_populates="reservation", uselist=True)  # 1..0..1

    # 1..0..1 relationship with Reservation table and ChannelRef table (Reservation table is parent)
    channel_ref = relationship("ChannelRef", back_populates="reservation", uselist=True)  # 1..0..1

    # 1..1..* relationship with Reservation table and ReservationItem table (Reservation table is parent)
    reservation_item = relationship("ReservationItem", back_populates="reservation", uselist=True)  # 1..1..*


class RelatedPartyRef(Base):
    __tablename__ = 'related_party_ref'

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    href: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(255))

    # 1..1 relationship with Reservation table and RelatedPartyRef table (RelatedPartyRef table is child)
    reservation_id = Annotated[int, ForeignKey("reservation.id")]
    reservation = relationship("Reservation", back_populates="related_party_ref", uselist=False)  # 1..1


# For future reference - not used in this example
class ChannelRef(Base):
    __tablename__ = 'channel_ref'

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    href: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    referredType: Mapped[str] = mapped_column(String(255))

    # 1..0..1 relationship with Reservation table and ChannelRef table (ChannelRef table is child)
    reservation_id = Annotated[int, ForeignKey("reservation.id")]
    reservation = relationship("Reservation", back_populates="channel_ref", uselist=True)  # 1..0..1


class ProductOfferingRef(Base):
    __tablename__ = 'product_offering_ref'

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    href: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    referredType: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))

    # 1..1 relationship with Reservation table and ProductOfferingRef table (ProductOfferingRef table is child)
    reservation_id = Annotated[int, ForeignKey("reservation.id")]
    reservation = relationship("Reservation", back_populates="product_offering_ref", uselist=False)  # 1..1


class RequestedPeriod(Base):
    __tablename__ = 'requested_period'

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    baseType: Mapped[str] = mapped_column(String(255))
    schemaLocation: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255))
    dayofweek: Mapped[str] = mapped_column(String(255))
    fromToDateTime: Mapped[str] = mapped_column(String(255))
    rangeInterval: Mapped[str] = mapped_column(String(255))
    validFor: Mapped[str] = mapped_column(String(255))

    # 1..0..1 relationship with Reservation table and RequestedPeriod table (RequestedPeriod table is child)
    reservation_id = Annotated[int, ForeignKey("reservation.id")]
    reservation = relationship("Reservation", back_populates="requested_period", uselist=True)  # 1..0..1


class ReservationItem(Base):
    __tablename__ = 'reservation_item'

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    baseType: Mapped[str] = mapped_column(String(255))
    schemaLocation: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255))
    quantity: Mapped[str] = mapped_column(String(255))
    subReservationState: Mapped[str] = mapped_column(String(255))

    # 1..1 relationship with Reservation table and ReservationItem table (ReservationItem table is child)
    reservation_id = Annotated[int, ForeignKey("reservation.id")]
    reservation_item = relationship("ReservationItem", back_populates="reservation_item", uselist=False)  # 1..1

    # 1..0 relationship with ReservationItem table and AppliedCapacityAmount table (ReservationItem table is parent)
    applied_capacity_amount = relationship("AppliedCapacityAmount", back_populates="reservation_item", uselist=True)

    # 1..1 relationship with ReservationItem table and ResourceCapacityDemand table (ReservationItem table is parent)
    resource_capacity_demand = relationship("ResourceCapacityDemand", back_populates="reservation_item",
                                            uselist=False)  # 1..1


class AppliedCapacityAmount(Base):
    __tablename__ = 'applied_capacity_amount'

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    baseType: Mapped[str] = mapped_column(String(255))
    schemaLocation: Mapped[str] = mapped_column(String(255))
    type: Mapped[int] = mapped_column(String(255))
    appliedDemandAmount: Mapped[str] = mapped_column(String(255))

    # 1..0 relationship with ReservationItem table and AppliedCapacityAmount table (AppliedCapacityAmount table is
    # child)
    reservation_item_id = Annotated[int, ForeignKey("reservation_item.id")]
    reservation_item = relationship("ReservationItem", back_populates="applied_capacity_amount", uselist=True)

    # 0..1 ..0..* relationship with AppliedCapacityAmount table and ResourceRef table (AppliedCapacityAmount table is
    # parent)
    resource_ref = relationship("ResourceRef", back_populates="applied_capacity_amount", uselist=True)


class ResourceRef(Base):
    __tablename__ = 'resource_ref'

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    href: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    referredType: Mapped[str] = mapped_column(String(255))
    resourceCharacteristic: Mapped[str] = mapped_column(String(255))
    value: Mapped[str] = mapped_column(String(255))

    # 0..1 ..0..* relationship with AppliedCapacityAmount table and ResourceRef table (ResourceRef table is child)
    applied_capacity_amount_id = Annotated[int, ForeignKey("applied_capacity_amount.id")]
    applied_capacity_amount = relationship("AppliedCapacityAmount", back_populates="resource_ref", uselist=True)


class ResourceCapacityDemand(Base):
    __tablename__ = 'resource_capacity_demand'

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    baseType: Mapped[str] = mapped_column(String(255))
    schemaLocation: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255))
    capacityDemandAmount: Mapped[str] = mapped_column(String(255))

    # 1..1 relationship with ReservationItem table and ResourceCapacityDemand table (ResourceCapacityDemand table is
    # child)
    reservation_item_id = Annotated[int, ForeignKey("reservation_item.id")]
    reservation_item = relationship("ReservationItem", back_populates="resource_capacity_demand", uselist=False)  # 1..1

    # 1..0..1 relationship with ResourceCapacityDemand table and PlaceRef table (ResourceCapacityDemand table is parent)
    place_ref = relationship("PlaceRef", back_populates="resource_capacity_demand", uselist=True)

    # 1..0..1 relationship with ResourceCapacityDemand table and ApplicationTimePeriod table (ResourceCapacityDemand
    # table is parent)
    applicable_time_period = relationship("ApplicableTimePeriod", back_populates="resource_capacity_demand",
                                          uselist=True)

    # 1..1 relationship with ResourceCapacityDemand table and ResourcePoolRef table (ResourceCapacityDemand table is
    # parent)
    resource_pool_ref = relationship("ResourcePoolRef", back_populates="resource_capacity_demand",
                                     uselist=False)  # 1..1


class PlaceRef(Base):
    __tablename__ = 'place_ref'

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    href: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    referredType: Mapped[str] = mapped_column(String(255))

    # 1..0..1 relationship with ResourceCapacityDemand table and PlaceRef table (PlaceRef table is child)
    resource_capacity_demand_id = Annotated[int, ForeignKey("resource_capacity_demand.id")]
    resource_capacity_demand = relationship("ResourceCapacityDemand", back_populates="place_ref",
                                            uselist=True)  # 1..0..1


class ApplicableTimePeriod(Base):
    __tablename__ = 'applicable_time_period'

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    baseType: Mapped[str] = mapped_column(String(255))
    schemaLocation: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255))
    dayofweek: Mapped[str] = mapped_column(String(255))
    fromToDateTime: Mapped[str] = mapped_column(String(255))
    rangeInterval: Mapped[str] = mapped_column(String(255))
    validFor: Mapped[str] = mapped_column(String(255))

    # 1..0..1 relationship with ResourceCapacityDemand table and ApplicableTimePeriod table (ApplicableTimePeriod
    # table is child)
    resource_capacity_demand_id = Annotated[int, ForeignKey("resource_capacity_demand.id")]
    resource_capacity_demand = relationship("ResourceCapacityDemand", back_populates="applicable_time_period",
                                            uselist=True)  # 1..0..1


class ResourcePoolRef(Base):
    __tablename__ = 'resource_pool_ref'

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    href: Mapped[str] = mapped_column(String(255))
    referredType: Mapped[str] = mapped_column(String(255))

    # 1..1 relationship with ResourceCapacityDemand table and ResourcePoolRef table (ResourcePoolRef table is child)
    resource_capacity_demand_id = Annotated[int, ForeignKey("resource_capacity_demand.id")]
    resource_capacity_demand = relationship("ResourceCapacityDemand", back_populates="resource_pool_ref",
                                            uselist=False)  # 1..1

    # 1..0..1 relationship with ResourcePoolRef table and ResourceCollectionRef table (ResourcePoolRef table is parent)
    resource_collection_ref = relationship("ResourceCollectionRef", back_populates="resource_pool_ref", uselist=True)


class ResourceCollectionRef(Base):
    __tablename__ = 'resource_collection_ref'

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    href: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    referredType: Mapped[str] = mapped_column(String(255))
    objectId: Mapped[str] = mapped_column(String(255))

    # 1..0..1 relationship with ResourcePoolRef table and ResourceCollectionRef table (ResourceCollectionRef table is
    # child)
    resource_pool_ref_id = Annotated[int, ForeignKey("resource_pool_ref.id")]
    resource_pool_ref = relationship("ResourcePoolRef", back_populates="resource_collection_ref",
                                     uselist=True)  # 1..0..1
