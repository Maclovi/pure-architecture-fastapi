#!/bin/bash

bash scripts/test.sh "$@"

coverage combine
coverage report --show-missing --sort=cover --precision=2

rm .coverage*
