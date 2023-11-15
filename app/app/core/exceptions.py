from typing import Dict, Optional

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException
from pydantic import BaseModel, ConfigDict, Field


class ErrorMessage(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    code: str
    reason: str
    message: str
    status: str
    reference_error: str = Field(..., alias="referenceError")
    base_type: str = Field(..., alias="@baseType")
    schema_location: str = Field(..., alias="@schemaLocation")
    type: str = Field(..., alias="@type")


class AppException(HTTPException):
    pass


class BadRequestError(AppException):
    def __init__(
        self,
        message: str,
        headers: dict[str, str] | None = None,
    ):
        status_code = status.HTTP_400_BAD_REQUEST

        super().__init__(
            detail=jsonable_encoder(
                ErrorMessage(
                    code=str(status_code),
                    reason="Bad Request",
                    message=message,
                    status="TBD",
                    reference_error="TBD",
                    base_type="TBD",
                    schema_location="TBD",
                    type="TBD",
                )
            ),
            headers=headers,
            status_code=status_code,
        )


class ConflictError(HTTPException):
    def __init__(
        self,
        message: str,
        headers: dict[str, str] | None = None,
    ):
        status_code = status.HTTP_409_CONFLICT

        super().__init__(
            detail=jsonable_encoder(
                ErrorMessage(
                    code=str(status_code),
                    reason="Not Found",
                    message=message,
                    status="TBD",
                    reference_error="TBD",
                    base_type="TBD",
                    schema_location="TBD",
                    type="TBD",
                )
            ),
            headers=headers,
            status_code=status_code,
        )


class NotFoundError(AppException):
    def __init__(
        self,
        message: str,
        headers: dict[str, str] | None = None,
    ):
        status_code = status.HTTP_404_NOT_FOUND

        super().__init__(
            detail=jsonable_encoder(
                ErrorMessage(
                    code=str(status_code),
                    reason="Not Found",
                    message=message,
                    status="TBD",
                    reference_error="TBD",
                    base_type="TBD",
                    schema_location="TBD",
                    type="TBD",
                )
            ),
            headers=headers,
            status_code=status_code,
        )
