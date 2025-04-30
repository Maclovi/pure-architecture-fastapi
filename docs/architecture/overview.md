# Architecture Overview

The Cats API is built using **Clean Architecture** principles, ensuring a modular, testable, and maintainable codebase. This section provides an overview of the architectural design.

## Project Structure

The codebase is organized as follows:

- **`src/cats/`**: Core application code
  - **`application/`**: Business logic (use cases)
  - **`entities/`**: Business models and value objects
  - **`infrastructure/`**: External integrations (e.g., database, observability)
  - **`presentation/`**: API endpoints and routing
  - **`web.py`**: Application entry point
- **`tests/`**: Unit and integration tests
- **`deploy/`**: Deployment configurations (Docker, Nginx, Grafana, etc.)
- **Configuration**: `.env.dist`, `pyproject.toml`, `alembic.ini`

## Key Components

- **FastAPI**: Powers the RESTful API.
- **SQLAlchemy/Alembic**: Manages database interactions and migrations.
- **Dishka**: Handles dependency injection.
- **Observability**: Integrates Prometheus, Grafana, Loki, and Tempo for monitoring.
- **CI/CD**: GitHub Actions for testing, building, and deployment.

## Layers

The application follows Clean Architecture with two primary layers:

1. **Inner Layer**: Business logic (`src/cats/application`, `src/cats/entities`)

   - Independent of external tools.
   - Uses Python standard library only.
   - Communicates via interfaces.

2. **External Layer**: Tools and integrations (`src/cats/infrastructure`, `src/cats/presentation`)
   - Includes database, HTTP server, and observability tools.
   - Interacts with the inner layer through interfaces.

Learn more in the [Clean Architecture](clean-architecture.md) section.
