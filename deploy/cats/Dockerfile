FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder
WORKDIR /app

COPY ./pyproject.toml ./alembic.ini ./deploy/cats/entrypoint.sh ./
COPY ./src ./src

RUN uv pip install --system --no-cache --target dependencies ".[prod]"


FROM python:3.12-slim as production
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "/app/dependencies"

RUN apt-get update && apt-get install -y curl

COPY --from=builder /app/ ./
