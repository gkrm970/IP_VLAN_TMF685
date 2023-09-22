# TMF685 - Resource pool management models

# standard library import
from typing import Annotated

# third party import
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.engine import default
from sqlalchemy.orm import relationship, mapped_column, Mapped

# local import
from app.db.base_class import Base

str250 = Annotated[str, 250,]
intpk = Annotated[int, mapped_column(primary_key=True),]
optional_str250 = Annotated[str, 250, None]


class ResourceCollectionRef(Base):
    __tablename__ = 'resource_collection_ref'

    id: Mapped[intpk]
    href: Mapped[optional_str250]
    name: Mapped[optional_str250]
    referredType: Mapped[optional_str250]
    objectId: Mapped[optional_str250]

    resource_pool_id: Annotated[int, ForeignKey("resource_pool.id")]


# ResourcePool
class ResourcePool(Base):
    __tablename__ = 'resource_pool'

    id: Mapped[intpk]
    baseType = mapped_column()
    schemaLocation: Mapped[optional_str250]
    type: Mapped[optional_str250]
    description: Mapped[optional_str250]
    href: Mapped[optional_str250]
    name: Mapped[optional_str250]
    relatedParty: Mapped[optional_str250]

    resource_collection_ref = relationship("ResourceCollectionRef", back_populates="resource_pool",
                                           uselist=False)  # 1..1
    capacity = relationship("Capacity", back_populates="resource_pool")  # 0..n


class Capacity(Base):
    __tablename__ = 'capacity'

    id: Mapped[intpk]
    baseType: Mapped[optional_str250]
    schemaLocation: Mapped[optional_str250]
    type: Mapped[optional_str250]
    planned_or_actual_capacity: Mapped[optional_str250]

    resource_pool_id = Annotated[int, ForeignKey("resource_pool.id")]
    resource_pool = relationship("ResourcePool", back_populates="capacity")  # 0..1


class ApplicableTimePeriod(Base):
    __tablename__ = 'applicable_time_period'

    id: Mapped[intpk]
    baseType: Mapped[optional_str250]
    schemaLocation: Mapped[optional_str250]
    type: Mapped[optional_str250]
    dayofweek: Mapped[optional_str250]
    fromToDateTime: Mapped[optional_str250]
    rangeInterval: Mapped[optional_str250]
    validFor: Mapped[optional_str250]

    capacity_id = Annotated[int, ForeignKey("capacity.id")]


class GraphicalPlaceRef(Base):
    __tablename__ = 'graphical_place_ref'

    id: Mapped[intpk]
    href: Mapped[optional_str250]
    referredType: Mapped[optional_str250]

    capacity_id = Annotated[int, ForeignKey("capacity.id")]


class CapacityRef(Base):
    __tablename__ = 'capacity_ref'

    id: Mapped[intpk]

    capacity_id = Annotated[int, ForeignKey("capacity.id")]


class CapacitySpecRef(Base):
    __tablename__ = 'capacity_spec_ref'

    id: Mapped[intpk]
    href: Mapped[optional_str250]
    referredType: Mapped[optional_str250]

    capacity_id = Annotated[int, ForeignKey("capacity.id")]


class CapacityAmount(Base):
    __tablename__ = 'capacity_amount'

    id: Mapped[intpk]
    capacityAmount: Mapped[optional_str250]
    capacityAmountFrom: Mapped[optional_str250]
    capacityAmountTo: Mapped[optional_str250]
    rangeInterval: Mapped[optional_str250]

    capacity_id = Annotated[int, ForeignKey("capacity.id")]


class AppliedCapacityAmount(Base):
    __tablename__ = 'applied_capacity_amount'

    id: Mapped[intpk]
    baseType: Mapped[optional_str250]
    schemaLocation: Mapped[optional_str250]
    type: Mapped[optional_str250]
    appliedDemandAmount: Mapped[optional_str250]
    capacityAmount_id = Annotated[int, ForeignKey("capacity_amount.id")]


class ResourceCapacityDemand(Base):
    __tablename__ = 'resource_capacity_demand'

    id: Mapped[intpk]
    baseType: Mapped[optional_str250]
    schemaLocation: Mapped[optional_str250]
    type: Mapped[optional_str250]
    capacityDemandAmount: Mapped[optional_str250]

    applied_capacity_amount_id = Annotated[int, ForeignKey("applied_capacity_amount.id")]


class PlaceRef(Base):
    __tablename__ = 'place_ref'

    id: Mapped[intpk]
    href: Mapped[optional_str250]
    referredType: Mapped[optional_str250]
    name: Mapped[optional_str250]

    resource_capacity_demand_id = Annotated[int, ForeignKey("resource_capacity_demand.id")]

# endregion
