from dataclasses import dataclass
from uuid import UUID

from typing_extensions import override


class ApplicationError(Exception):
    """Base class for all application-specific exceptions.

    Provides a consistent interface for
        error messages across all application errors.
    All domain-specific exceptions should inherit from this class.

    Attributes:
        message: Read-only property returning
            a human-readable error description.
    """

    @property
    def message(self) -> str:
        """Provides a human-readable description of the error.

        Returns:
            str: Default error message for application errors.
        """
        return "Application error occurred"


@dataclass(eq=False)
class EntityNotFoundError(ApplicationError):
    """Exception raised when a requested entity cannot be found in the system.

    This error typically occurs when attempting to access, update, or delete
    an entity with a non-existent identifier.

    Attributes:
        oid: The identifier that was used in the failed lookup operation.
            Can be either an integer or UUID depending on the entity type.

    Note:
        - Inherits from ApplicationError to maintain consistent error handling
        - Disables equality comparison (eq=False) as exceptions are typically
          compared by type rather than content
    """

    oid: int | UUID

    @property
    @override
    def message(self) -> str:
        """Generates a descriptive error message
            including the missing entity ID.

        Returns:
            str: Formatted message indicating which entity was not found.
        """
        return f"Entity with id={self.oid} not found"
