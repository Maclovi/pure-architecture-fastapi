from cats.application.common.errors.base import ApplicationError
from cats.entities.common.errors import DomainError


def test_domain_error() -> None:
    assert DomainError().message == "Domain error occurred"


def test_application_error() -> None:
    assert ApplicationError().message == "Application error occurred"
