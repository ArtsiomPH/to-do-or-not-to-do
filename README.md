# ToDo list. (Django + PostgreSQL + Docker)

[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2FArtsiomPH%2Fto-do-or-not-to-do%2Fbadge%3Fref%3Ddev&style=flat)](https://actions-badge.atrox.dev/ArtsiomPH/to-do-or-not-to-do/goto?ref=dev)

## Description

Technical task for Andersen. Architecture based on [example-django-mssql-docker](https://github.com/tgrx/example-django-mssql-docker) by [Alexander Sidorov](https://github.com/tgrx).

Includes:
1. [Task](https://taskfile.dev).
2. [Poetry](https://python-poetry.org/).
3. DB driver [PostgreSQL](https://www.psycopg.org/docs/).
4. [Non-root user](https://betterprogramming.pub/running-a-container-with-a-non-root-user-e35830d1f42a).
5. [Caches](https://docs.docker.com/build/cache/).

## Usage

See `.env.sample` for examples. `WEBAPP_` is a prefix for env vars.

After successful build & run,
you can open [http://localhost:8000/](http://localhost:8000/).

Default admin credentials: *login* - *admin*, *password* - *admin1234*.

## Installation

Before doing something, make sure that you have

1. copied `.env.sample` to `.env`
2. modified values in `.env` according to your realm

### Docker

First, hit `docker compose build`.

Next, hit `task docker-up` OR `docker compose up -d`.

### Bare metal

#### Mac OS

If you have [brew](https://brew.sh/), [pyenv](https://github.com/pyenv/pyenv) and [Task](https://taskfile.dev/) installed, this would be enough:

`task setup-toolchain`

#### Linux

If you have [pyenv](https://github.com/pyenv/pyenv) and [Task](https://taskfile.dev/) installed, this might be enough:

`task setup-toolchain`

I haven't checked yet this way, please send me a feedback in case of any bug.

#### Other

1. install [Python 3.11.7](https://www.python.org/downloads/release/python-3117/)
2. install [Poetry 1.6.1](https://python-poetry.org/docs/#installation)
3. bind Python 3.11.7 to the cloned directory (this project)
4. create venv and install dependencies: `poetry install --with dev --sync`
5. double-check your `.env`
6. start webapp with `poetry run python manage.py runserver 0.0.0.0:8000`
