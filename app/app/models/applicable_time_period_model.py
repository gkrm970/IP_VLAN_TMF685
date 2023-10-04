import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import Annotated

from app.db.base import Base

datetime = Annotated[DateTime, datetime.datetime]


class ApplicableTimePeriod(Base):
    __tablename__ = 'applicable_time_period'

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    baseType: Mapped[str] = mapped_column(String(255))
    schemaLocation: Mapped[str] = mapped_column(String(255))
    type: Mapped[str] = mapped_column(String(255))
    dayOfWeek: Mapped[str] = mapped_column(String(255))
    fromToDateTime: Mapped[DateTime] = mapped_column(String(255))
    rangeInterval: Mapped[str] = mapped_column(String(255))
    validFor: Mapped[str] = mapped_column(String(255))

    # 1..0..1 relationship with ResourceCapacityDemand table and ApplicableTimePeriod table (ApplicableTimePeriod
    # table is child)
    resource_capacity_demand_id: Mapped[str] = mapped_column(String), ForeignKey("resource_capacity_demand.id")
    resource_capacity_demand = relationship("ResourceCapacityDemand",
                                            back_populates="applicable_time_period")  # 1..0..1
