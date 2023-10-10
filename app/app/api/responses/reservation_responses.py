from typing import Any

from app.core.exceptions import ErrorMessage

_NOT_FOUND = "Not Found"


_base_responses: dict[int | str, dict[str, Any]] = {
    400: {"description": "Bad Request", "model": ErrorMessage},
    401: {"description": "Unauthorized", "model": ErrorMessage},
    403: {"description": "Forbidden", "model": ErrorMessage},
    405: {"description": "Method Not Allowed", "model": ErrorMessage},
    409: {"description": "Conflict", "model": ErrorMessage},
    500: {"description": "Internal Server Error", "model": ErrorMessage},
}


_not_found_response: dict[int | str, dict[str, Any]] = {
    404: {"description": _NOT_FOUND},
}

create_responses = {
    201: {"description": "Created"},
    **_base_responses,
}

get_responses = {
    200: {"description": "Success"},
    **_not_found_response,
    **_base_responses,
}

delete_responses = {
    204: {"description": "Deleted"},
    **_not_found_response,
    **_base_responses,
}

update_responses = {
    200: {"description": "Updated"},
    **_not_found_response,
    **_base_responses,
}
