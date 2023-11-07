from app import log, schemas
from app.core.exceptions import BadRequestError

_resource_field_alias_name_mapping: dict[str, str] = {
    field_info.alias or field_name: field_name
    for field_name, field_info in schemas.ResourcePool.model_fields.items()
}


_resource_schema_field_aliases: set[str] = {
    field_info.alias or field_name
    for field_name, field_info in schemas.ResourcePool.model_fields.items()
}


_mandatory_resource_schema_field_aliases: set[str] = {
    field_info.alias or field_name
    for field_name, field_info in schemas.ResourcePoolCreate.model_fields.items()
    if field_info.is_required()
}


def _ensure_query_fields_are_valid(query_fields: set[str]) -> None:
    if not query_fields.issubset(_resource_schema_field_aliases):
        raise BadRequestError(
            message=(
                f"The following query fields are invalid: "
                f"{', '.join(query_fields.difference(_resource_schema_field_aliases))}"
            )
        )

    log.debug("Query fields parameters are valid")


def _include_mandatory_fields(query_fields: set[str]) -> set[str]:
    return query_fields | _mandatory_resource_schema_field_aliases


def get_include_fields_for_response(fields_query: str) -> set[str] | None:
    # The default fields query parameter on the GET endpoints is an empty string.
    # None return value means all fields will be included in the API response.
    if not fields_query:
        log.debug("No query field parameter defined")
        return None

    fields = {field.strip() for field in fields_query.split(",")}

    _ensure_query_fields_are_valid(fields)

    fields = _include_mandatory_fields(fields)

    field_aliases = {_resource_field_alias_name_mapping[field] for field in fields}

    log.debug(f"Included field aliases: {', '.join(field_aliases)}")

    return field_aliases
