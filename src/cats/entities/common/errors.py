class DomainError(Exception):
    """Base exception class for domain layer errors.

    Provides a consistent interface for error messages across all
        domain-specific.
    exceptions. All domain-level errors should inherit from this class.

    Attributes:
        message: A human-readable description of the error.
            Default implementation returns a generic message,
            which should be overridden by subclasses.

    Note:
        - Serves as the root of the domain error hierarchy
        - Uses property decorator for consistent error message interface
        - Follows the convention of rich exceptions with additional attributes
    """

    @property
    def message(self) -> str:
        """Provides a default error message for domain errors.

        Returns:
            str: Generic domain error message. Subclasses should override this
                to provide more specific error information.
        """
        return "Domain error occurred"


class FieldError(DomainError):
    """Exception raised when domain field validation fails.

    Indicates that a value assigned to a domain object's field violates
    business rules or invariants.

    Note:
        - Inherits from DomainError to maintain consistent error handling
        - Used for validation failures in value objects and entities
        - Typically caught and converted to appropriate application errors
        - The default message from DomainError is usually sufficient,
          but can be overridden for specific field validation cases
    """
