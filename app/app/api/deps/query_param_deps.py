from fastapi import Query

FieldsQuery = Query(description="Comma-separated properties to be provided in response")

LimitQuery = Query(
    description="Requested number of resources to be provided in response",
)

OffsetQuery = Query(
    description="Requested index for start of resources to be provided in response",
)
