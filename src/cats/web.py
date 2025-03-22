import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import cast

from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from cats.bootstrap import (
    setup_configs,
    setup_exc_handlers,
    setup_logger,
    setup_map_tables,
    setup_middlewares,
    setup_routes,
)
from cats.infrastructure.configs import APIConfig, PostgresConfig
from cats.ioc import setup_providers

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI, /) -> AsyncIterator[None]:
    yield None
    await cast("AsyncContainer", app.state.dishka_container).close()


def create_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
        version="1.0.0",
        root_path="/api",
        servers=[
            {"url": "/api/v1", "description": "Version 1"},
        ],
    )
    configs = setup_configs()
    context = {APIConfig: configs.api, PostgresConfig: configs.db}
    container = make_async_container(*setup_providers(), context=context)
    setup_logger()
    setup_map_tables()
    setup_routes(app)
    setup_exc_handlers(app)
    setup_middlewares(app, api_config=configs.api)
    setup_dishka(container, app)
    logger.info("App created", extra={"app_version": app.version})
    return app
