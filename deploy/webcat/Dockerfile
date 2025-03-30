FROM ghcr.io/astral-sh/uv:python3.12-alpine as builder
WORKDIR /app

COPY ./pyproject.toml ./alembic.ini ./deploy/webcat/server.sh ./
COPY ./src ./src

RUN uv pip install --system --no-cache --target dependencies .


FROM python:3.12-alpine as production
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1 \
    PYTHONUNBUFFERED 1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PYTHONPATH "/app/dependencies"

COPY --from=builder /app/ ./
