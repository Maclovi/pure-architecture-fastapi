FROM python:3.12.7-slim as builder
WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/app/src/"

COPY ./pyproject.toml ./pyproject.toml
RUN pip install uv && uv pip install --no-cache --system -r pyproject.toml

COPY  ./ ./
