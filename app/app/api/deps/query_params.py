from typing import Annotated

from fastapi import Query

FieldsQuery = Annotated[
    str,
    Query(description="Comma-separated properties to be provided in response"),
]

LimitQuery = Annotated[
    int,
    Query(
        description="Requested number of resources to be provided in response",
    ),
]

OffsetQuery = Annotated[
    int,
    Query(
        description=(
            "Requested index for start of resources to be provided in response"
        ),
    ),
]
