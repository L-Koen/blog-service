# Define an alias for the specific python version used in this file.
FROM python:3-slim AS python

# Python build stage
FROM python AS python-build-stage

# Install apt packages
RUN apt update && apt install --no-install-recommends -y \
  build-essential \
  git \
  && apt clean \
  && rm -rf /var/lib/apt/lists/*
  

# Requirements are installed here to ensure they will be cached.
COPY ./requirements/base.txt .

# Create Python Dependency and Sub-Dependency Wheels.
RUN pip wheel --wheel-dir /usr/src/app/wheels -r base.txt

# Python 'run' stage
FROM python AS python-run-stage

ARG APP_HOME=/app

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR ${APP_HOME}

# Install required system dependencies and clean up apt lists
RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# Copy python dependency wheels from python-build-stage
COPY --from=python-build-stage /usr/src/app/wheels /wheels/

# Use wheels to install python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
  && rm -rf /wheels/

# Copy entrypoint and start scripts
COPY ./compose/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint && chmod +x /entrypoint

COPY ./compose/start /start
RUN sed -i 's/\r$//g' /start && chmod +x /start

# Set user and group to work with non-root user and volumes
ARG UID
ARG GID

RUN groupadd --gid $GID mygroup \
    && useradd --uid $UID --gid $GID --create-home myuser

USER myuser

# Copy application code to WORKDIR
# Not used for now, mounting folder
# COPY . ${APP_HOME}

ENTRYPOINT ["/entrypoint"]
