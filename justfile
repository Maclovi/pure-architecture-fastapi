set dotenv-load

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

[doc("Start main application")]
@run:
    python -m alembic upgrade head
    python -m uvicorn --factory cats.web:create_app --host $UVICORN_HOST --port $UVICORN_PORT

[doc("Run all containers")]
[group("infra")]
@up:
  docker compose up -d

[doc("Stop all containers")]
[group("infra")]
@stop:
  docker compose stop

[doc("Down all containers")]
[group("infra")]
@down:
  docker compose down

[doc("Up only postgres")]
[group("infra")]
@up-postgres:
    docker compose up -d postgres

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
@test: up-postgres
    coverage run -m pytest -x --ff
    just stop

[doc("Run test with coverage")]
[group("Test")]
@cov: test
    coverage combine
    coverage report --show-missing --skip-covered --sort=cover --precision=2
    rm .coverage*
    just stop
