from pydantic import BaseModel

from cats.application.common.persistence.filters import SortOrder


class ExceptionSchema(BaseModel):
    """Standard error response schema for API exceptions.

    Attributes:
        detail: Human-readable error message describing the problem.

    Used as:
    - Base format for all error responses
    - Consistent structure across all error cases
    """

    detail: str


class PaginationSchema(BaseModel):
    """Base pagination parameters for list endpoints.

    Attributes:
        offset: Number of items to skip (optional).
        limit: Maximum number of items to return (optional).
        order: Sort direction (ASC or DESC), defaults to ASC.

    Notes:
    - When not specified, offset and limit typically use server defaults
    - SortOrder is an enum with ASC/DESC values
    """

    offset: int | None = None
    limit: int | None = None
    order: SortOrder = SortOrder.ASC


class CatFiltersSchema(BaseModel):
    """Filtering parameters for cat-related queries.

    Attributes:
        breed: Filter cats by breed name (optional).
        color: Filter cats by color (optional).

    Notes:
    - All filters are optional
    - Multiple filters are combined with AND logic
    - Filter values are typically case-insensitive
    """

    breed: str | None = None
    color: str | None = None


class CatsAllSchema(PaginationSchema, CatFiltersSchema):
    """Combined schema for listing cats with pagination and filtering.

    Inherits:
    - PaginationSchema (offset, limit, order)
    - CatFiltersSchema (breed, color)

    Represents the complete query parameter set for:
    - GET /cats endpoint
    - Other cat listing operations

    Example URL:
    /cats?offset=0&limit=10&order=ASC&breed=siamese&color=white
    """
