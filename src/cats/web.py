import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dishka import AsyncContainer, make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from cats.bootstrap import (
    setup_configs,
    setup_exc_handlers,
    setup_map_tables,
    setup_middlewares,
    setup_observability,
    setup_routes,
)
from cats.infrastructure.configs import ASGIConfig, PostgresConfig
from cats.ioc import setup_providers

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI, /) -> AsyncIterator[None]:
    yield None
    container: AsyncContainer = app.state.dishka_container
    await container.close()


def create_app_tests() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
        version="1.0.0",
        root_path="/api",
        debug=True,
    )
    configs = setup_configs()
    context = {ASGIConfig: configs.asgi, PostgresConfig: configs.db}
    container = make_async_container(*setup_providers(), context=context)
    setup_map_tables()
    setup_routes(app)
    setup_exc_handlers(app)
    setup_middlewares(app, api_config=configs.asgi)
    setup_dishka(container, app)
    logger.info("App created", extra={"app_version": app.version})
    return app


def create_app_production() -> FastAPI:  # pragma: no cover
    configs = setup_configs()
    app = FastAPI(
        lifespan=lifespan,
        default_response_class=ORJSONResponse,
        version="1.0.0",
        root_path="/api",
        debug=configs.asgi.fastapi_debug,
    )
    context = {ASGIConfig: configs.asgi, PostgresConfig: configs.db}
    container = make_async_container(*setup_providers(), context=context)
    setup_map_tables()
    setup_routes(app)
    setup_exc_handlers(app)
    setup_observability(app, configs.observability)
    setup_middlewares(app, api_config=configs.asgi)
    setup_dishka(container, app)
    logger.info("App created", extra={"app_version": app.version})
    return app
