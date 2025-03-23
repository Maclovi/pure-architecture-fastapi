#!/bin/sh
set -e

python -m alembic upgrade head
python -m uvicorn --factory cats.web:create_app --host "0.0.0.0" --port $UVICORN_PORT
