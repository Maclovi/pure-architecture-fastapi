from typing import TYPE_CHECKING

from starlette.middleware.cors import CORSMiddleware

from cats.presentation.http.middlewares.tracing import LoggingMiddleware

if TYPE_CHECKING:
    from fastapi import FastAPI

    from cats.infrastructure.configs import APIConfig


def setup_middlewares(app: "FastAPI", /, api_config: "APIConfig") -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            f"http://localhost:{api_config.port}",
            f"http://{api_config.host}:{api_config.port}",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(LoggingMiddleware)