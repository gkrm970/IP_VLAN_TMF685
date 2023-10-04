import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import Annotated

from app import models
from app.db.base import Base

datetime = Annotated[DateTime, datetime.datetime]



class ResourceCollectionRef(Base):
    __tablename__ = 'resource_collection_ref'

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    href: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255))
    referredType: Mapped[str] = mapped_column(String(255))
    objectId: Mapped[str] = mapped_column(String(255))

    # 1..0..1 relationship with ResourcePoolRef table and ResourceCollectionRef table (ResourceCollectionRef table is
    # child)
    resource_pool_ref_id: Mapped[str] = mapped_column(String), ForeignKey("resource_pool_ref.id")
    resource_pool_ref = relationship("ResourcePoolRef", back_populates="resource_collection_ref")  # 1..0..1
