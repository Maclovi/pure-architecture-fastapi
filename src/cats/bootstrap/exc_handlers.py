from functools import partial

from fastapi import FastAPI
from starlette import status as code

from cats.application.common.errors.base import EntityNotFoundError
from cats.entities.common.errors import FieldError
from cats.presentation.http.common.exc_handlers import validate


def setup_exc_handlers(app: FastAPI) -> None:
    app.add_exception_handler(
        FieldError,
        partial(validate, status=code.HTTP_422_UNPROCESSABLE_ENTITY),
    )
    app.add_exception_handler(
        EntityNotFoundError,
        partial(validate, status=code.HTTP_404_NOT_FOUND),
    )
