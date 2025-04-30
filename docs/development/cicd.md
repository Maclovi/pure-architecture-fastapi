# CI/CD

The Cats API uses **GitHub Actions** for continuous integration and deployment, ensuring automated testing, building, and deployment.

## Workflows

Located in `.github/workflows/`:

### pr-tests.yaml:

- **Triggers**: Pull requests, daily schedule, manual dispatch.
- **Jobs**:
  - **pre-commit-check**: Runs linters and formatters (Ruff, codespell).
  - **test-basic**: Runs tests across Python versions (3.10–3.13) with PostgreSQL.
- **Services**: PostgreSQL container for integration tests.

### build-and-push.yaml:

- **Triggers**: Manual dispatch, merged pull requests.
- **Job**: Builds and pushes Docker images to GitHub Container Registry (GHCR).
- **Environments**: Supports `stage` and `prod`.

### deploy.yaml:

- **Triggers**: Manual dispatch, successful `build-and-push` runs.
- **Job**: Deploys to a remote server via SSH, using Docker Compose.
- **Files**: Copies `docker-compose.stage.yaml` and `deploy/` directory.

## Configuration

### Dependabot (`.github/dependabot.yaml`):

- Updates GitHub Actions, pip, and Docker Compose dependencies weekly.
- Targets the `develop` branch.

### Secrets:

- `REGISTRY_PAT`: For GHCR access.
- `SSH_USERNAME`, `SSH_KEY`, `SSH_PORT`, `HOST`: For deployment.
- Defined in GitHub repository settings.

## Example Workflow

From `pr-tests.yaml`:

```yaml
name: Run all tests
on:
  pull_request:
    types: [opened, synchronize, ready_for_review]
jobs:
  test-basic:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12", "3.13"]
    services:
      postgres:
        image: postgres:alpine
        env:
          POSTGRES_DB: test
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: coverage run -m pytest -x --ff
```

## Running Locally

Simulate CI tests:

```bash
just cov
```

See for details on test execution.
