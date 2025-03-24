set dotenv-load

DOCKER_COMPOSE_DEV := "docker-compose.dev.yaml"

[doc("All command information")]
[private]
default:
  @just --list --unsorted --list-heading $'Cats commands…\n'

[doc("Prepare venv and repo for developing")]
@bootstrap:
    cp .env.dist .env
    python3 -m pip install uv
    uv pip install -e ".[dev]"
    pre-commit
    pre-commit install

[doc("Sync latest versions of packages")]
@venv-sync:
    uv pip install -e ".[dev]"

[doc("Run server application")]
@serve: infra
    ./deploy/webcat/server.sh ; just stop

[doc("Run all containers")]
[group("infra")]
@up *args:
  docker compose -f {{ DOCKER_COMPOSE_DEV }} up -d {{ args }}

[doc("Run all containers except web-backend")]
[group("infra")]
@infra:
    docker compose -f {{ DOCKER_COMPOSE_DEV }} up -d db

[doc("Stop all containers")]
[group("infra")]
@stop:
  docker compose -f {{ DOCKER_COMPOSE_DEV }} stop

[doc("Down all containers")]
[group("infra")]
@down:
  docker compose -f {{ DOCKER_COMPOSE_DEV }} down
  docker image prune -f

[doc("Lint check")]
[group("Lint")]
@lint:
    echo "Run ruff check..." && ruff check --exit-non-zero-on-fix
    echo "Run ruff format..." && ruff format
    echo "Run codespell..." && codespell

[doc("Static analysis")]
[group("Static")]
@static:
    echo "Run mypy.." && mypy --config-file pyproject.toml
    echo "Run bandit..." && bandit -c pyproject.toml -r src
    echo "Run semgrep..." && semgrep scan --config auto --error

[doc("Run test")]
[group("Test")]
@test: infra
    coverage run -m pytest -x --ff
    just stop

[doc("Run test with coverage")]
[group("Test")]
@cov: test
    coverage combine
    coverage report --show-missing --skip-covered --sort=cover --precision=2
    rm .coverage*
    just stop
