import re
from typing import Any

from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(AsyncAttrs, DeclarativeBase):
    # All tables have IDs, this is here to avoid type-checking errors from mypy
    id: Any

    # This performs snake_case conversion and generates the name of the table
    # from the classname automatically, the declared_attr.directive indicates to PEP 484
    # typing tools that the given method is not dealing with Mapped attributes:
    @classmethod
    @declared_attr.directive
    def __tablename__(cls) -> str:
        # This regexp contains two capturing groups:
        #   - the first matches a single character
        #   - the second matches a capital letter, followed by at least one, but
        #     possibly more lowercase letters
        # In the replacement, the first capturing group (\1) will be separated by an
        # underscore (_) from the second capturing group (\2)
        name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", cls.__name__)

        # In this second regexp, there are two capturing groups again:
        #   - the first one matches a single lowercase or digit character
        #   - the second one matches a capital letter
        # In the replacement, the first capturing group (\1) will be separated by an
        # underscore (_) from the second capturing group (\2)
        name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()

        return name.replace("__", "_")
