from dataclasses import dataclass

from typing_extensions import override

from cats.entities.common.errors import FieldError


@dataclass(eq=False)
class CatAgeMinError(FieldError):
    """Exception raised when a cat's age is below the minimum allowed value.

    Attributes:
        limit: The minimum age requirement that wasn't met.

    Note:
        - Inherits from FieldError for consistent field validation handling
        - Disables equality comparison (eq=False) since
            exceptions are typically.
          compared by type rather than content
    """

    limit: int

    @property
    @override
    def message(self) -> str:
        """Provides a descriptive error message about minimum age requirement.

        Returns:
            str: Formatted message indicating the required minimum age.
        """
        return (
            f"The minimum age of the cat should not be less than {self.limit}"
        )


@dataclass(eq=False)
class CatAgeMaxError(FieldError):
    """Exception raised when a cat's age exceeds the maximum allowed value.

    Attributes:
        age: The actual age that exceeded the maximum limit.

    Note:
        - Inherits from FieldError to maintain validation error consistency
        - Used when age validation fails upper bound checks
    """

    age: int

    @property
    @override
    def message(self) -> str:
        """Provides a descriptive error message about maximum age limit.

        Returns:
            str: Formatted message indicating the maximum allowed age.
        """
        return f"The maximum age of a cat should not exceed {self.age!r}"


@dataclass(eq=False)
class CatColorMinLengthError(FieldError):
    """Exception raised when a cat's color description is too short.

    Attributes:
        length: The minimum required length that wasn't met.

    Note:
        - Part of the cat color validation error hierarchy
        - Ensures color descriptions meet minimum length requirements
    """

    length: int

    @property
    @override
    def message(self) -> str:
        """Provides a descriptive error message about minimum color length.

        Returns:
            str: Formatted message indicating the required minimum length.
        """
        return f"The color length should not be less than {self.length}"


@dataclass(eq=False)
class CatColorMaxLengthError(FieldError):
    """Exception raised when a cat's color description is too long.

    Attributes:
        length: The maximum allowed length that was exceeded.

    Note:
        - Completes the cat color validation error set with max length check
        - Works with CatColorMinLengthError for full length validation
    """

    length: int

    @property
    @override
    def message(self) -> str:
        """Provides a descriptive error message about maximum color length.

        Returns:
            str: Formatted message indicating the allowed maximum length.
        """
        return f"The color length should not exceed {self.length}"


@dataclass(eq=False)
class CatDescriptionLengthError(FieldError):
    """Exception raised when a cat's description exceeds length limits.

    Attributes:
        length: The maximum allowed description length that was exceeded.

    Note:
        - Specifically for cat description field validation
        - Ensures descriptions remain within reasonable size limits
    """

    length: int

    @property
    @override
    def message(self) -> str:
        """Provides a descriptive error message about description length limit.

        Returns:
            str: Formatted message indicating the maximum allowed length.
        """
        return f"The description length should not exceed {self.length!r}"
