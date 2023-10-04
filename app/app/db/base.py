# Declarative base class, that contains the metadata of the database tables
from app.db.base_class import Base  # noqa: F401

# Import all the models, so that Base has them before being imported by Alembic
from app.models import Reservation  # noqa: F401
from app.models import Resource  # noqa: F401
