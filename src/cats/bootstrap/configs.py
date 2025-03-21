from os import environ as env
from typing import NamedTuple

from cats.infrastructure.configs import APIConfig, PostgresConfig


class Configs(NamedTuple):
    db: PostgresConfig
    api: APIConfig


def load_configs() -> Configs:
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
