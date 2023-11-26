from sqlalchemy import ARRAY, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base_class import BaseDbModel


class VlanAllocation(BaseDbModel):
    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    used_vlan_numbers: Mapped[list[int]] = mapped_column(ARRAY(Integer))
    resource_pool_id: Mapped[str] = mapped_column(String(255), default=None)
