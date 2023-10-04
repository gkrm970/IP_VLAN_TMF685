import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import Annotated

from app import models
from app.db.base import Base

datetime = Annotated[DateTime, datetime.datetime]


class ResourceRef(Base):
    __tablename__ = 'resource_ref'

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    href: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    referredType: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255))
    resourceCharacteristic: Mapped[str] = mapped_column(String(255))

    # 0..1 ..0..* relationship with AppliedCapacityAmount table and ResourceRef table (ResourceRef table is child)
    applied_capacity_amount_id: Mapped[str] = mapped_column(String), ForeignKey("applied_capacity_amount.id")
    applied_capacity_amount = relationship("AppliedCapacityAmount", back_populates="resource_ref")
