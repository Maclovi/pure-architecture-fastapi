import logging
from os import environ as env

from asgi_monitor.integrations.fastapi import (
    MetricsConfig,
    TracingConfig,
    setup_metrics,
    setup_tracing,
)
from asgi_monitor.logging import configure_logging
from fastapi import APIRouter, FastAPI
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter,
)
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from starlette.middleware.cors import CORSMiddleware

from cats.infrastructure.configs import (
    ASGIConfig,
    Configs,
    ObservabilityConfig,
    PostgresConfig,
)
from cats.infrastructure.persistence.models.breed import map_breed_table
from cats.infrastructure.persistence.models.cat import map_cat_table
from cats.presentation.http.v1.common.exc_handlers import map_exc_handlers
from cats.presentation.http.v1.routes import breeds, cats, healthcheck, index


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
            debug=env["SQLALCHEMY_DEBUG"] == "1",
        ),
        asgi=ASGIConfig(
            host=env["UVICORN_HOST"],
            port=int(env["UVICORN_PORT"]),
        ),
        observability=ObservabilityConfig(
            app_name=env.get("APP_NAME", "Some Name"),
            grpc_endpoint=env.get("GRPC_ENDPOINT", "Some Endpoint"),
        ),
    )


def setup_routes(app: FastAPI, /) -> None:
    router_v1 = APIRouter(prefix="/v1")
    router_v1.include_router(cats.router)
    router_v1.include_router(breeds.router)
    router_v1.include_router(index.router)
    router_v1.include_router(healthcheck.router)

    app.include_router(router_v1)


def setup_middlewares(app: FastAPI, /, api_config: ASGIConfig) -> None:
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


def setup_exc_handlers(app: FastAPI, /) -> None:
    map_exc_handlers(app)


def setup_observability(
    app: FastAPI,
    /,
    observability_config: ObservabilityConfig,
) -> None:  # pragma: no cover
    configure_logging(level=logging.INFO, json_format=True, include_trace=True)

    resource = Resource.create(
        attributes={
            "service.name": observability_config.app_name,
            "compose_service": observability_config.app_name,
        },
    )
    tracer_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer_provider)
    tracer_provider.add_span_processor(
        BatchSpanProcessor(
            OTLPSpanExporter(endpoint=observability_config.grpc_endpoint),
        ),
    )
    trace_config = TracingConfig(tracer_provider=tracer_provider)
    setup_tracing(app=app, config=trace_config)

    metrics_config = MetricsConfig(
        app_name=observability_config.app_name,
        include_trace_exemplar=True,
    )
    setup_metrics(app=app, config=metrics_config)
