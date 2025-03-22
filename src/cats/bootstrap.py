import logging
import sys
from os import environ as env

from fastapi import APIRouter, FastAPI
from pythonjsonlogger.orjson import OrjsonFormatter
from starlette.middleware.cors import CORSMiddleware

from cats.infrastructure.configs import APIConfig, Configs, PostgresConfig
from cats.infrastructure.persistence.models.breed import map_breed_table
from cats.infrastructure.persistence.models.cat import map_cat_table
from cats.presentation.http.v1.common.exc_handlers import map_exc_handlers
from cats.presentation.http.v1.middlewares.tracing import LoggingMiddleware
from cats.presentation.http.v1.routes import breeds, cats, index


def setup_map_tables() -> None:
    map_cat_table()
    map_breed_table()


def setup_configs() -> Configs:
    return Configs(
        db=PostgresConfig(
            user=env["POSTGRES_USER"],
            password=env["POSTGRES_PASSWORD"],
            host=env["POSTGRES_HOST"],
            port=env["POSTGRES_PORT"],
            db_name=env["POSTGRES_DB"],
            debug=env["POSTGRES_DEBUG"] == "true",
        ),
        api=APIConfig(
            host=env["UVICORN_HOST"],
            port=env["UVICORN_PORT"],
        ),
    )


def setup_routes(app: FastAPI, /) -> None:
    router_v1 = APIRouter(prefix="/v1")
    router_v1.include_router(cats.router)
    router_v1.include_router(breeds.router)
    router_v1.include_router(index.router)

    app.include_router(router_v1)


def setup_middlewares(app: FastAPI, /, api_config: APIConfig) -> None:
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


def setup_exc_handlers(app: FastAPI) -> None:
    map_exc_handlers(app)


def setup_logger() -> None:
    fmt = "%(levelname)s %(asctime)s %(name)s %(funcName)s %(message)s"
    formatter = OrjsonFormatter(fmt)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, handlers=[stream_handler])
