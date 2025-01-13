from typing import TYPE_CHECKING, ClassVar, cast

from starlette.responses import JSONResponse

if TYPE_CHECKING:
    from starlette.requests import Request

    class StubError(Exception):
        message: ClassVar[str]


async def validate(_: "Request", exc: Exception, status: int) -> JSONResponse:
    exc = cast("StubError", exc)
    return JSONResponse(content={"detail": exc.message}, status_code=status)
