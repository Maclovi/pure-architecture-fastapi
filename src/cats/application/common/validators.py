from typing import TypeVar

from cats.application.common.errors.base import EntityNotFoundError

T = TypeVar("T")


def validate_empty(cat: T | None, oid: int) -> T:
    if cat is None:
        raise EntityNotFoundError(oid=oid)
    return cat
