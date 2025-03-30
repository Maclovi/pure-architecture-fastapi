from dataclasses import dataclass

from cats.entities.breed.errors import (
    BreedNameMaxlengthError,
    BreedNameMinlengthError,
)


@dataclass(slots=True, frozen=True, eq=True, unsafe_hash=True)
class BreedName:
    """Value object representing a validated cat breed name.

    Encapsulates the business rules and validation logic for breed names,
    ensuring only properly formatted names can be used in the domain.

    Attributes:
        value: The validated breed name string.

    Raises:
        BreedNameMinlengthError: If name is shorter
            than minimum length (2 chars).
        BreedNameMaxlengthError: If name exceeds maximum length (50 chars).

    Note:
        - Immutable (frozen) to prevent modification after creation
        - Uses slots for memory efficiency
        - Implements equality comparison (eq=True)
        - Hashable (unsafe_hash=True) for use in sets/dicts
        - Validation occurs during initialization
        - Follows value object pattern from Domain-Driven Design

    Example:
        >>> try:
        ...     name = BreedName("Siamese")  # Valid
        ...     invalid = BreedName("A")  # Raises BreedNameMinlengthError
        ... except BreedNameMinlengthError as e:
        ...     print(e.message)
    """

    value: str

    def __post_init__(self) -> None:
        """Validates the breed name against business rules.

        Performs length validation:
        - Minimum length: 2 characters
        - Maximum length: 50 characters

        Raises:
            BreedNameMinlengthError: If name is too short.
            BreedNameMaxlengthError: If name is too long.
        """
        breed_min_length = 2
        breed_max_length = 50
        if len(self.value) < breed_min_length:
            raise BreedNameMinlengthError(breed_min_length)
        if len(self.value) > breed_max_length:
            raise BreedNameMaxlengthError(breed_max_length)
