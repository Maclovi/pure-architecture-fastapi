import logging
from functools import partial
from typing import TYPE_CHECKING, ClassVar, cast

from fastapi import FastAPI
from starlette import status as code
from starlette.requests import Request
from starlette.responses import JSONResponse

from cats.application.common.errors.base import EntityNotFoundError
from cats.entities.common.errors import FieldError

logger = logging.getLogger(__name__)


if TYPE_CHECKING:

    class StubError(Exception):
        message: ClassVar[str]


async def validate(_: "Request", exc: Exception, status: int) -> JSONResponse:
    """Generic exception handler for validation and business logic errors.

    Converts exceptions with a 'message' attribute
        into standardized JSON error responses.

    Args:
        _: The incoming request (unused)
        exc: The exception instance being handled
        status: HTTP status code to return

    Returns:
        JSONResponse: Formatted error response containing:
            - detail: Error message from the exception

    Note:
        Used as base handler for FieldError and EntityNotFoundError cases.
    """
    exc = cast("StubError", exc)
    return JSONResponse(content={"detail": exc.message}, status_code=status)


async def internal_trouble(_: Request, __: Exception) -> JSONResponse:  # pyright: ignore[reportUnusedParameter]
    """Fallback handler for unexpected server errors.

    Returns a generic 500 error response when unhandled exceptions occur.

    Args:
        _: The incoming request (unused)
        __: The uncaught exception (unused)

    Returns:
        JSONResponse: Standardized internal server error response:
            - detail: Generic error message

    Note:
        - Should be registered last in the exception handler chain
        - Acts as catch-all for unhandled exceptions
        - Logs should be used to track actual error details
    """
    return JSONResponse(
        status_code=code.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )


def map_exc_handlers(app: FastAPI) -> None:
    """Registers exception handlers for the FastAPI application.

    Sets up handlers for:
        - FieldError (422 Unprocessable Entity)
        - EntityNotFoundError (404 Not Found)
        - Generic Exception (500 Internal Server Error)

    Args:
        app: FastAPI application instance to configure

    Note:
        - Handlers are registered in specific order (generic last)
        - FieldError typically represents validation failures
        - EntityNotFoundError indicates missing resources
        - The internal_trouble handler should remain last
    """
    app.add_exception_handler(
        FieldError,
        partial(validate, status=code.HTTP_422_UNPROCESSABLE_ENTITY),
    )
    app.add_exception_handler(
        EntityNotFoundError,
        partial(validate, status=code.HTTP_404_NOT_FOUND),
    )
    app.add_exception_handler(Exception, internal_trouble)
