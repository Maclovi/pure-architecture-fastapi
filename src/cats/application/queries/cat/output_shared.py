from dataclasses import dataclass

from cats.application.common.persistence.view_models import CatView


@dataclass(slots=True, frozen=True)
class CatsOutput:
    """Data transfer object for paginated cat list API responses.

    Represents a page of cat records along with total count
        information for pagination.
    Used as the standardized output format for cat listing endpoints.

    Attributes:
        total: The complete count of cats matching the query filters,
            ignoring pagination.
        cats: A page of cat records, represented as CatView instances.
            The number of records matches the requested page size
                or fewer if at the end of the dataset.

    Notes:
        - Immutable (frozen) to prevent accidental
            modification of response data
        - Uses __slots__ for memory efficiency in high-volume responses
        - Maintains consistency with pagination best practices
        - Always returned by GetCatsQueryHandler operations

    Example:
        Typical JSON serialization format:
        {
            "total": 42,
            "cats": [
                {
                    "cat_id": 1,
                    "breed": "Siamese",
                    "age": 2,
                    "color": "white",
                    "description": "Very vocal"
                },
                {
                    "cat_id": 2,
                    "breed": "Persian",
                    "age": 5,
                    "color": "gray",
                    "description": "Calm and fluffy"
                }
            ]
        }
    """

    total: int
    cats: list[CatView]
