#!/bin/sh

set -e  # Exit if any command fails

MYUID="$(id -u)" MYGID="$(id -g)" docker compose run --rm blog-service pytest -v
MYUID="$(id -u)" MYGID="$(id -g)" docker compose run --rm blog-service mypy /app/src/
MYUID="$(id -u)" MYGID="$(id -g)" docker compose run --rm blog-service flake8 /app/src/
MYUID="$(id -u)" MYGID="$(id -g)" docker compose run --rm blog-service black --check --diff --color /app/src/