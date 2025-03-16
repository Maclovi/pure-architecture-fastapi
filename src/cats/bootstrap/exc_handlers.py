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
    exc = cast("StubError", exc)
    return JSONResponse(content={"detail": exc.message}, status_code=status)


async def internal_trouble(_: Request, __: Exception) -> JSONResponse:  # pyright: ignore[reportUnusedParameter]
    return JSONResponse(  # pragma: no cover
        status_code=code.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )


def setup_exc_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        FieldError,
        partial(validate, status=code.HTTP_422_UNPROCESSABLE_ENTITY),
    )
    app.add_exception_handler(
        EntityNotFoundError,
        partial(validate, status=code.HTTP_404_NOT_FOUND),
    )
    # should be in the end
    app.add_exception_handler(Exception, internal_trouble)
