# Configuration

The Cats API follows the **Twelve-Factor App** methodology, using environment variables for configuration to ensure flexibility and security.

## Configuration File

- **Location**: `src/cats/infrastructure/configs.py`
- **Sample**: `.env.dist`

## Environment Variables

Key variables defined in `.env.dist` include:

| Variable            | Description                        | Default                  |
| ------------------- | ---------------------------------- | ------------------------ |
| `POSTGRES_USER`     | PostgreSQL username                | `postgres`               |
| `POSTGRES_PASSWORD` | PostgreSQL password                | `postgres`               |
| `POSTGRES_HOST`     | PostgreSQL host                    | `127.0.0.1`              |
| `POSTGRES_PORT`     | PostgreSQL port                    | `5432`                   |
| `POSTGRES_DB`       | PostgreSQL database name           | `postgres`               |
| `SQLALCHEMY_DEBUG`  | Enable SQLAlchemy debug logs       | `1`                      |
| `UVICORN_HOST`      | Uvicorn server host                | `0.0.0.0`                |
| `UVICORN_PORT`      | Uvicorn server port                | `8080`                   |
| `FASTAPI_DEBUG`     | Enable FastAPI debug mode          | `0`                      |
| `APP_NAME`          | Application name for observability | `cats`                   |
| `GRPC_ENDPOINT`     | Tempo endpoint for tracing         | `http://cats.tempo:4317` |

## Usage

1. **Copy Sample Environment**:

   ```bash
   cp .env.dist .env
   ```

2. **Customize**: Edit .env to adjust settings for your environment.
3. **Apply**: The just bootstrap command automatically uses .env. For Docker, ensure .env is loaded:

```bash
export $(cat .env | xargs)
just up
```

## Database Migrations

Apply migrations using Alembic:

```bash
python -m alembic upgrade head
```
