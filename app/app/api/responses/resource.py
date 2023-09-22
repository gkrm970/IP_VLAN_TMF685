_base_responses: dict[int | str, dict[str, str]] = {
    400: {"description": "Bad Request"},
    401: {"description": "Unauthorized"},
    403: {"description": "Forbidden"},
    405: {"description": "Method Not Allowed"},
    409: {"description": "Conflict"},
    500: {"description": "Internal Server Error"},
}

create_responses = {
    201: {"description": "Created"},
    **_base_responses,
}

get_responses = {
    200: {"description": "Success"},
    404: {"description": "Not Found"},
    **_base_responses,
}

delete_responses = {
    204: {"description": "Deleted"},
    **_base_responses,
}

update_responses = {
    200: {"description": "Updated"},
    404: {"description": "Not Found"},
    **_base_responses,
}
