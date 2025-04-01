FROM ghcr.io/astral-sh/uv:python3.12-alpine as builder
WORKDIR /app

COPY ./pyproject.toml ./alembic.ini ./deploy/cats/server.sh ./
COPY ./src ./src

RUN uv pip install --system --no-cache --target dependencies ".[prod]"


FROM python:3.12-alpine as production
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "/app/dependencies"

COPY --from=builder /app/ ./
