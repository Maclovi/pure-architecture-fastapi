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
    """Async context manager for FastAPI application lifecycle management.

    Handles the startup and shutdown events of the FastAPI application.
    Specifically ensures proper cleanup
        of Dishka container resources on shutdown.

    Args:
        app: FastAPI application instance. Positional-only parameter.

    Yields:
        None: Indicates successful entry into the context.

    Note:
        The actual resource cleanup (Dishka container closure)
            happens after yield, during the application shutdown phase.
    """
    yield None
    await cast("AsyncContainer", app.state.dishka_container).close()


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
    """Creates and configures a FastAPI application
        instance with all dependencies.

    Performs comprehensive application setup including:
    - Configuration initialization
    - Dependency injection container setup
    - Database mapping
    - Route registration
    - Exception handlers
    - Observability tools
    - Middleware stack
    - Dishka integration

    Returns:
        FastAPI: Fully configured application instance ready for use.

    Side Effects:
        - Configures global application state
        - Initializes database mappings
        - Sets up observability tools
        - Registers all route handlers

    Example:
        >>> app = create_app()
        >>> uvicorn.run(app)
    """
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
