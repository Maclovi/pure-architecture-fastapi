from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CatView:
    """View model representing a cat entity for read operations.

    This immutable data structure provides a standardized
        representation of cat data
    when returned from queries, ensuring consistent serialization
        in API responses.

    Attributes:
        cat_id: Unique identifier of the cat.
        breed: Breed name (optional, may be None for mixed-breed cats).
        age: Age of the cat in years.
        color: Primary color of the cat's coat.
        description: Descriptive text about the cat's
            appearance or personality.

    Notes:
        - Frozen to ensure thread-safety and prevent accidental modification
        - Uses slots for memory efficiency
        - Designed for read-only presentation of cat data
        - Typically used in query responses and list views

    Example JSON representation:
        {
            "cat_id": 42,
            "breed": "Siamese",
            "age": 3,
            "color": "cream",
            "description": "Playful and vocal"
        }
    """

    cat_id: int
    breed: str | None
    age: int
    color: str
    description: str
