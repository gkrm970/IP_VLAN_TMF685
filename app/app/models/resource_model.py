import datetime

from sqlalchemy import Column, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import Annotated

from app.db.base import Base

datetime = Annotated[DateTime, datetime.datetime]


class Resource(Base):
    __tablename__ = 'resource'
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    baseType: Mapped[str] = mapped_column(String(255))
    schemaLocation: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255))
    href: Mapped[str] = mapped_column(String(255))
    relatedParty: Mapped[str | None] = mapped_column(String(255))


class ResourcePool(Base):
    __tablename__ = 'resource_pool'

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    schemaLocation: Mapped[str] = mapped_column(String(255))
    baseType: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    href: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    relatedParty: Mapped[str] = mapped_column(String(255))

    # # 1..0 relationship with ResourcePool table and ResourceCollectionRef table (ResourcePool table is parent)
    # resource_collection_ref = relationship("ResourceCollectionRef", back_populates="resource_pool", uselist=True)
    #
    # # 1..0 relationship with ResourcePool table and Capacity table (ResourcePool table is parent)
    # capacity = relationship("Capacity", back_populates="resource_pool", uselist=True)


class Capacity(Base):
    __tablename__ = 'capacity'

    id: Mapped[int] = mapped_column(String(255), primary_key=True, index=True)
    baseType: Mapped[str] = mapped_column(String(255))
    schemaLocation: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255))
    planned_or_actual_capacity: Mapped[str] = mapped_column(String(255))

    # # 1..1 relationship with Capacity table and ApplicableTimePeriod table (Capacity table is parent)
    # applicable_time_period_resource = relationship("ApplicableTimePeriod", back_populates="capacity", uselist=False)  # 1..1
    #
    # # 1..0 relationship with ResourcePool table and Capacity table (Resource table is parent)
    # resource_pool_id = Annotated[int, ForeignKey('resource_pool.id')]
    # resource_pool = relationship("ResourcePool", back_populates="capacity", uselist=False)  # 1..0
    #
    # # 1..0..* relationship with Capacity table and CapacitySpecRef table (Capacity table is parent)
    # capacity_spec_ref = relationship("CapacitySpecRef", back_populates="capacity", uselist=True)  # 1..0..*
    #
    # # 1..0..1 relationship with Capacity table and GraphicalPlaceRef table (Capacity table is parent)
    # graphical_place_ref = relationship("GraphicalPlaceRef", back_populates="capacity", uselist=True)  # 1..0..1
    #
    # # 1..1 relationship with Capacity table and capacityRef table (Capacity table is parent)
    # capacity_ref = relationship("capacityRef", back_populates="capacity", uselist=True)
    #
    # # 1..1 relationship with Capacity table and capacityAmount table (Capacity table is parent)
    # capacity_amount = relationship("capacityAmount", back_populates="capacity")  # 1..1


class CapacitySpecRef(Base):
    __tablename__ = 'capacity_spec_ref'

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    href: Mapped[str] = mapped_column(String(255))
    referredType: Mapped[str] = mapped_column(String(255))

    # # 1..1 relationship with Capacity table and CapacitySpecRef table (CapacitySpecRef table is child)
    # capacity_id = Annotated[int, ForeignKey('capacity.id')]
    # capacity = relationship("Capacity", back_populates="capacity_spec_ref", uselist=False)  # 1..1
    #

class ApplicableTimePeriod(Base):
    __tablename__ = 'applicable_time_period_resource'

    id: Mapped[int] = mapped_column(String(255), primary_key=True, index=True)
    baseType: Mapped[str] = mapped_column(String(255))
    schemaLocation: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255))
    dayofweek: Mapped[str] = mapped_column(String(255))
    fromToDateTime: Mapped[str] = mapped_column(String(255))
    rangeInterval: Mapped[str] = mapped_column(String(255))
    validFor: Mapped[str] = mapped_column(String(255))

    # # 1..1 relationship with Capacity table and ApplicableTimePeriod table (ApplicableTimePeriod table is child)
    # capacity_id = Annotated[int, ForeignKey('capacity.id')]
    # capacity = relationship("Capacity", back_populates="applicable_time_period_resource", uselist=False)  # 1..1


class GraphicalPlaceRef(Base):
    __tablename__ = 'graphical_place_ref'

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    href: Mapped[str] = mapped_column(String(255))
    referredType: Mapped[str] = mapped_column(String(255))

    # # 1..0..1 relationship with Capacity table and GraphicalPlaceRef table (GraphicalPlaceRef table is child)
    # capacity_id = Annotated[int, ForeignKey('capacity.id')]
    # capacity = relationship("Capacity", back_populates="graphical_place_ref", uselist=True)  # 1..0..1


class CapacityRef(Base):
    __tablename__ = 'capacity_ref'

    id: Mapped[int] = mapped_column(String(255), primary_key=True, index=True)

    # # 1..0..* relationship with Capacity table and CapacityRef table (CapacityRef table is child)
    # capacity_id = Annotated[int, ForeignKey('capacity.id')]


class CapacityAmount(Base):
    __tablename__ = 'capacity_amount'

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    capacityAmount: Mapped[str] = mapped_column(String(255))
    capacityAmountFrom: Mapped[str] = mapped_column(String(255))
    capacityAmountTo: Mapped[str] = mapped_column(String(255))
    rangeInterval: Mapped[str] = mapped_column(String(255))

    # # 1..1 relationship with Capacity table and CapacityAmount table (CapacityAmount table is child)
    # capacity_id = Annotated[int, ForeignKey('capacity.id')]
    # capacity = relationship("Capacity", back_populates="capacity_amount", uselist=False)  # 1..1
    #
    # # 1..0..* relationship with CapacityAmount table and AppliedCapacityAmount table (CapacityAmount table is parent)
    # applied_capacity_amount_resource = relationship("AppliedCapacityAmount", back_populates="capacity_amount", uselist=True)


class AppliedCapacityAmount(Base):
    __tablename__ = 'applied_capacity_amount_resource'

    id: Mapped[int] = mapped_column(String(255), primary_key=True, index=True)
    baseType: Mapped[str] = mapped_column(String(255))
    schemaLocation: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255))
    appliedDemandAmount: Mapped[str] = mapped_column(String(255))

    # # 1..0..* relationship with CapacityAmount table and AppliedCapacityAmount table (AppliedCapacityAmount table is
    # # child)
    # capacity_amount_id = Annotated[int, ForeignKey('capacity_amount.id')]
    # capacity_amount = relationship("CapacityAmount", back_populates="applied_capacity_amount_resource", uselist=True)  # 1..0..*
    #
    # # 1..0..* relationship with AppliedCapacityAmount table and ResourceCapacityDemand table (AppliedCapacityAmount
    # # table is parent)
    # applied_capacity_amount_resource = relationship("ResourceCapacityDemand", back_populates="applied_capacity_amount_resource",
    #                                         uselist=True)


class ResourceCapacityDemand(Base):
    __tablename__ = 'resource_capacity_demand_resource'

    id: Mapped[int] = mapped_column(String(255), primary_key=True, index=True)
    baseType: Mapped[str] = mapped_column(String(255))
    schemaLocation: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255))
    capacityDemandAmount: Mapped[str] = mapped_column(String(255))

    # # 1..0..* relationship with AppliedCapacityAmount table and ResourceCapacityDemand table (ResourceCapacityDemand
    # # table is child)
    # applied_capacity_amount_resource_id = Annotated[int, ForeignKey('applied_capacity_amount_resource.id')]
    # applied_capacity_amount_resource = relationship("AppliedCapacityAmount", back_populates="applied_capacity_amount_resource",
    #                                        uselist=True)  # 1..0..*
    #
    # # 1..0..* relationship with ResourceCapacityDemand table and PlaceRef table (ResourceCapacityDemand table is
    # parent) place_ref_resource = relationship("PlaceRef", back_populates="applied_capacity_amount_resource",
    # uselist=True)


class PlaceRef(Base):
    __tablename__ = 'place_ref_resource'

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    href: Mapped[str] = mapped_column(String(255))
    referredType: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))

    # # 1..0..* relationship with ResourceCapacityDemand table and PlaceRef table (PlaceRef table is child)
    # applied_capacity_amount_resource_id = Annotated[int, ForeignKey('applied_capacity_amount_resource.id')]
    # applied_capacity_amount_resource = relationship("ResourceCapacityDemand", back_populates="place_ref_resource",
    #                                         uselist=True)  # 1..0..*
