from typing import TypeVar

from cats.application.common.errors.base import EntityNotFoundError

T = TypeVar("T")


def validate_empty(cat: T | None, oid: int) -> T:
    """Validates that a retrieved entity exists or raises an appropriate error.

    This generic validation utility ensures null-checking consistency across
    the application layer for entity retrieval operations.

    Args:
        cat: The potentially None value returned from a lookup operation.
        oid: The identifier used in the lookup operation, for error reporting.

    Returns:
        The non-None cat value if it exists.

    Raises:
        EntityNotFoundError: If the cat value is None,
            indicating no entity was found with the specified identifier.

    Type Variables:
        T: The type of entity being validated.

    Example:
        >>> result = validate_empty(repository.find(123), 123)
        >>> # Either returns the entity or raises EntityNotFoundError
    """
    if cat is None:
        raise EntityNotFoundError(oid=oid)
    return cat
