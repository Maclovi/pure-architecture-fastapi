#!/bin/bash
set -e

alembic upgrade head
uvicorn --factory cats.web:create_app --host $UVICORN_HOST --port $UVICORN_PORT
