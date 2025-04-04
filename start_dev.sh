#!/bin/bash

MYUID="$(id -u)" MYGID="$(id -g)" RUN_MODE="django" docker compose --env-file .env.dev up --build