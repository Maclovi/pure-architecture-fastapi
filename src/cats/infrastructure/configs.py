from typing import NamedTuple


class PostgresConfig(NamedTuple):
    """Configuration container for PostgreSQL database connection settings.

    Attributes:
        user: Database username.
        password: Database password.
        host: Database server hostname or IP address.
        port: Database server port.
        db_name: Name of the database to connect to.
        debug: Flag to enable debug output for database operations.

    Properties:
        uri: Complete PostgreSQL connection URI in psycopg format.
    """

    user: str
    password: str
    host: str
    port: str
    db_name: str
    debug: bool

    @property
    def uri(self) -> str:
        """Generates a PostgreSQL connection URI.

        Returns:
            str: Connection string in format:
                postgresql+psycopg://user:password@host:port/db_name

        Note:
            - Uses psycopg driver for async operations
            - Includes all authentication credentials
            - Suitable for SQLAlchemy's create_async_engine
        """
        full_url = "postgresql+psycopg://"
        full_url += f"{self.user}:{self.password}"
        full_url += f"@{self.host}:{self.port}/{self.db_name}"
        return full_url


class ASGIConfig(NamedTuple):
    """Configuration container for ASGI server settings.

    Attributes:
        host: Interface to bind the server to (e.g., '0.0.0.0' or 'localhost').
        port: TCP port to listen on.
    """

    host: str
    port: int


class ObservabilityConfig(NamedTuple):
    """Observability config"""

    app_name: str
    grpc_endpoint: str


class Configs(NamedTuple):
    """Aggregate configuration container for all application settings.

    Groups together all configuration components needed by the application.

    Attributes:
        db: PostgreSQL database configuration.
        asgi: ASGI server configuration.
    """

    db: PostgresConfig
    asgi: ASGIConfig
    observability: ObservabilityConfig
