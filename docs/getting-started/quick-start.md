# Quick Start

This guide helps you get the Cats API up and running quickly.

## Local Development

1. **Ensure Installation**:
   Complete the [Installation](installation.md) steps.

2. **Start the Infrastructure**:
   Launch the database container:

   ```bash
   just infra
   ```

3. **Run the Server**: Start the FastAPI application:

   ```bash
   just serve
   ```

4. **Access the API**:
   - Swagger UI: http://localhost:8080/docs
   - Healthcheck: http://localhost:8080/v1/healthcheck/

## Full Docker Stack

To run all services (API, database, Grafana, Loki, etc.):

```bash
just up
```

- **API**: http://localhost:80/api
- **Grafana**: http://localhost/grafana (default credentials: admin/admin)

## Running Tests

Execute integration tests with coverage:

```bash
just cov
```
