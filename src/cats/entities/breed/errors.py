from dataclasses import dataclass

from typing_extensions import override

from cats.entities.common.errors import FieldError


@dataclass(eq=False)
class BreedNameMinlengthError(FieldError):
    """Exception raised when a breed name is too short.

    Indicates that a breed name failed minimum length validation.

    Attributes:
        length: The minimum required length that was not met.

    Note:
        - Inherits from FieldError to maintain consistent
            field validation handling
        - Disables equality comparison (eq=False) as exceptions are typically
          compared by type rather than content
        - The message includes the required minimum length
    """

    length: int

    @property
    @override
    def message(self) -> str:
        """Provides a descriptive error message about
            minimum length requirement.

        Returns:
            str: Formatted message indicating the required minimum length.
        """
        return f"The minimum length must not be less than {self.length!r}"


@dataclass(eq=False)
class BreedNameMaxlengthError(FieldError):
    """Exception raised when a breed name is too long.

    Indicates that a breed name failed maximum length validation.

    Attributes:
        length: The maximum allowed length that was exceeded.

    Note:
        - Inherits from FieldError to maintain consistent
            field validation handling
        - Disables equality comparison (eq=False)
        - The message includes the maximum allowed length
    """

    length: int

    @property
    @override
    def message(self) -> str:
        """Provides a descriptive error message
            about maximum length requirement.

        Returns:
            str: Formatted message indicating the allowed maximum length.
        """
        return f"Maximum length must be less than or equal to {self.length!r}"
