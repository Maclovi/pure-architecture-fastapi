FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
WORKDIR /app

ENV UV_COMPILE_BYTECODE 1
ENV UV_SYSTEM_PYTHON 1
ENV UV_NO_CACHE 1

COPY ./pyproject.toml ./
RUN uv pip install -r pyproject.toml --extra=prod --target dependencies

COPY ./src ./justfile ./alembic.ini ./


FROM python:3.12-slim-bookworm
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "/app/dependencies"

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    mkdir -p /usr/local/bin && \
    curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to /usr/local/bin && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    adduser --system --group --no-create-home appuser && \
    chown -R appuser:appuser /app

COPY --from=builder /app/ ./
USER appuser
