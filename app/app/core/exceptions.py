from typing import Optional, Dict

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field

_reference_error_alias: Literal["referenceError"] = "referenceError"
_base_type_alias: Literal["@baseType"] = "@baseType"
_schema_location_alias: Literal["@schemaLocation"] = "@schemaLocation"
_type_alias: Literal["@type"] = "@type"


class ErrorMessage(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    code: str
    reason: str
    message: str
    status: str
    reference_error: str = Field(..., alias=_reference_error_alias)
    base_type: str = Field(..., alias=_base_type_alias)
    schema_location: str = Field(..., alias=_schema_location_alias)
    type: str = Field(..., alias=_type_alias)


class BadRequestError(HTTPException):
    def __init__(
        self,
        message: str,
        headers: dict[str, str] | None = None,
    ):
        status_code = status.HTTP_400_BAD_REQUEST

        super().__init__(
            detail=jsonable_encoder(
                ErrorMessage(
                    **{
                        "code": str(status_code),
                        "reason": "Bad Request",
                        "message": message,
                        "status": "TBD",
                        _reference_error_alias: "TBD",
                        _base_type_alias: "TBD",
                        _schema_location_alias: "TBD",
                        _type_alias: "TBD",
                    },
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
                    **{
                        "code": str(status_code),
                        "reason": "Conflict",
                        "message": message,
                        "status": "TBD",
                        _reference_error_alias: "TBD",
                        _base_type_alias: "TBD",
                        _schema_location_alias: "TBD",
                        _type_alias: "TBD",
                    },
                )
            ),
            headers=headers,
            status_code=status_code,
        )


class UnauthorizedError(HTTPException):
    def __init__(
        self,
        message: str,
        headers: dict[str, str] | None = None,
    ):
        status_code = status.HTTP_401_UNAUTHORIZED

        super().__init__(
            detail=jsonable_encoder(
                ErrorMessage(
                    **{
                        "code": str(status_code),
                        "reason": "Unauthorized",
                        "message": message,
                        "status": "TBD",
                        _reference_error_alias: "TBD",
                        _base_type_alias: "TBD",
                        _schema_location_alias: "TBD",
                        _type_alias: "TBD",
                    },
                )
            ),
            headers=headers,
            status_code=status_code,
        )


class NotFoundError(HTTPException):
    def __init__(
        self,
        message: str,
        headers: dict[str, str] | None = None,
    ):
        status_code = status.HTTP_404_NOT_FOUND

        super().__init__(
            detail=jsonable_encoder(
                ErrorMessage(
                    **{
                        "code": str(status_code),
                        "reason": "Not Found",
                        "message": message,
                        "status": "TBD",
                        _reference_error_alias: "TBD",
                        _base_type_alias: "TBD",
                        _schema_location_alias: "TBD",
                        _type_alias: "TBD",
                    },
                )
            ),
            headers=headers,
            status_code=status_code,
        )


class InternalError(HTTPException):
    def __init__(
        self,
        message: str,
        headers: dict[str, str] | None = None,
    ):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        super().__init__(
            detail=jsonable_encoder(
                ErrorMessage(
                    **{
                        "code": str(status_code),
                        "reason": "Internal Server Error",
                        "message": message,
                        "status": "TBD",
                        _reference_error_alias: "TBD",
                        _base_type_alias: "TBD",
                        _schema_location_alias: "TBD",
                        _type_alias: "TBD",
                    },
                )
            ),
            headers=headers,
            status_code=status_code,
        )


async def validation_exception_handler(
    _request: Request, exc: RequestValidationError
) -> JSONResponse:
    message = f"{len(exc.errors())} validation errors"

    for index, err in enumerate(exc.errors(), start=1):
        message += f" || {index}. {err}"

    error = BadRequestError(message=message)

    return JSONResponse(
        content=jsonable_encoder(error.detail),
        status_code=error.status_code,
    )


def add_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
