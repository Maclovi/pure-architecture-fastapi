from dataclasses import dataclass
from os import environ as env


@dataclass(frozen=True, slots=True)
class PostgresConfig:
    user: str
    password: str
    host: str
    port: str
    db_name: str
    debug: bool

    @property
    def uri(self) -> str:
        return f"postgresql+psycopg://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"


@dataclass(frozen=True, slots=True)
class APIConfig:
    host: str
    port: str


@dataclass(frozen=True, slots=True)
class Configs:
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
