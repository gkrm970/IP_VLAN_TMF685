from typing import Optional


from sqlalchemy.orm import Session


from app import crud, models
from app.schemas.item import ItemCreate
from app.tests.utils.utils import random_lower_string


def create_random_item(db: Session) -> models.Item:
    title = random_lower_string()
    description = random_lower_string()
    item_in = ItemCreate(title=title, description=description)
    return crud.item.create(db=db, obj_in=item_in)
