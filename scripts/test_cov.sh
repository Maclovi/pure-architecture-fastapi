#!/bin/sh

bash scripts/test.sh "$@"

coverage combine
coverage report --show-missing --skip-covered --sort=cover --precision=2

rm .coverage*
