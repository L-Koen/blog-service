#!/bin/bash

MYUID="$(id -u)" MYGID="$(id -g)" docker compose --env-file .env.test up --build