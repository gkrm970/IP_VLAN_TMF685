import base64
from typing import Generator

from fastapi import status
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2AuthorizationCodeBearer
from jose import jwt
from pydantic import ValidationError

from sqlalchemy.orm import Session


from app import crud, models, schemas
from app.core import security
from app.core.config import settings

from app.db.session import SessionLocal


reusable_oauth2 = OAuth2AuthorizationCodeBearer(
    authorizationUrl=settings.AUTH_AUTHORIZATION_URL,
    tokenUrl=settings.AUTH_TOKEN_URL,
    refreshUrl=settings.AUTH_TOKEN_URL,
)



def get_db() -> Generator:
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        if db:
            db.close()


