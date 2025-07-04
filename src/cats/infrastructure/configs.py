from typing import NamedTuple


class PostgresConfig(NamedTuple):
    user: str
    password: str
    host: str
    port: str
    db_name: str
    debug: bool

    @property
    def uri(self) -> str:
        full_url = "postgresql+psycopg://"
        full_url += f"{self.user}:{self.password}"
        full_url += f"@{self.host}:{self.port}/{self.db_name}"
        return full_url


class ASGIConfig(NamedTuple):
    host: str
    port: int
    fastapi_debug: bool


class ObservabilityConfig(NamedTuple):
    app_name: str
    grpc_endpoint: str


class Configs(NamedTuple):
    db: PostgresConfig
    asgi: ASGIConfig
    observability: ObservabilityConfig
