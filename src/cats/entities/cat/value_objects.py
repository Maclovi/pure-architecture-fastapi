from dataclasses import dataclass

from cats.entities.cat.errors import (
    CatAgeMaxError,
    CatAgeMinError,
    CatColorMaxLengthError,
    CatColorMinLengthError,
    CatDescriptionLengthError,
)


@dataclass(slots=True, frozen=True, eq=True, unsafe_hash=True)
class CatAge:
    """Value object representing a validated cat age.

    Encapsulates business rules for valid cat ages, ensuring only properly
    formatted ages can be used in the domain.

    Attributes:
        value: The validated age in years (0-99).

    Raises:
        CatAgeMinError: If age is below minimum (0 years).
        CatAgeMaxError: If age exceeds maximum (99 years).

    Note:
        - Immutable (frozen) to prevent modification after validation
        - Uses slots for memory efficiency
        - Implements equality comparison (eq=True)
        - Hashable (unsafe_hash=True) for use in sets/dicts
        - Validation occurs during initialization
        - Follows value object pattern from Domain-Driven Design

    Example:
        >>> try:
        ...     age = CatAge(5)  # Valid
        ...     invalid = CatAge(-1)  # Raises CatAgeMinError
        ... except CatAgeMinError as e:
        ...     print(e.message)
    """

    value: int

    def __post_init__(self) -> None:
        """Validates the age against business rules.

        Performs range validation:
        - Minimum age: 0 years
        - Maximum age: 99 years
        """
        min_age = 0
        max_age = 99
        if self.value < min_age:
            raise CatAgeMinError(min_age)
        if self.value > max_age:
            raise CatAgeMaxError(max_age)


@dataclass(slots=True, frozen=True, eq=True, unsafe_hash=True)
class CatColor:
    """Value object representing a validated cat color.

    Encapsulates business rules for valid cat colors, ensuring only properly
    formatted color descriptions can be used in the domain.

    Attributes:
        value: The validated color description string.

    Raises:
        CatColorMinLengthError: If color is shorter
            than minimum length (3 chars).
        CatColorMaxLengthError: If color exceeds maximum length (50 chars).

    Note:
        - Immutable to maintain consistency after validation
        - Slots optimized for memory usage
        - Full equality comparison support
        - Hashable for collections
        - Validation occurs during initialization

    Example:
        >>> try:
        ...     color = CatColor("black")  # Valid
        ...     invalid = CatColor("b")  # Raises CatColorMinLengthError
        ... except CatColorMinLengthError as e:
        ...     print(e.message)
    """

    value: str

    def __post_init__(self) -> None:
        """Validates the color description against business rules.

        Performs length validation:
        - Minimum length: 3 characters
        - Maximum length: 50 characters
        """
        color_min_length = 3
        color_max_length = 50
        if len(self.value) < color_min_length:
            raise CatColorMinLengthError(color_min_length)
        if len(self.value) > color_max_length:
            raise CatColorMaxLengthError(color_max_length)


@dataclass(slots=True, frozen=True, eq=True, unsafe_hash=True)
class CatDescription:
    """Value object representing a validated cat description.

    Encapsulates business rules for valid cat descriptions, ensuring they
    remain within reasonable length limits.

    Attributes:
        value: The validated description string.

    Raises:
        CatDescriptionLengthError: If description exceeds
            maximum length (1000 chars).

    Note:
        - Immutable to prevent modification after validation
        - Memory efficient slots implementation
        - Full value object equality support
        - Hashable for use in collections
        - Only maximum length is enforced

    Example:
        >>> try:
        ...     desc = CatDescription("Friendly cat")  # Valid
        ...     invalid = CatDescription(
        ...         "x" * 1001
        ...     )  # Raises CatDescriptionLengthError
        ... except CatDescriptionLengthError as e:
        ...     print(e.message)
    """

    value: str

    def __post_init__(self) -> None:
        """Validates the description against business rules.

        Performs length validation:
        - Maximum length: 1000 characters
        (No minimum length requirement)
        """
        description_max_length = 1000
        if len(self.value) > description_max_length:
            raise CatDescriptionLengthError(description_max_length)
