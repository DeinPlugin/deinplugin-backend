FROM python:3.11.0-slim-bullseye as base

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1

FROM base as python-deps

ENV PYTHONUNBUFFERED 1

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc && apt-get install -y apache2 apache2-dev python3-dev libpq-dev build-essential

COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy
RUN pipenv install mod_wsgi psycopg2

FROM base AS runtime

RUN apt-get update && apt-get install -y apache2 apache2-dev apache2-utils python3-dev libpq-dev build-essential cron

COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"

RUN mod_wsgi-express install-module > /etc/apache2/mods-available/wsgi.load

RUN a2enmod wsgi && a2enmod ssl


COPY ./deinplugin /var/www/deinplugin
COPY ./apache-config.conf /etc/apache2/sites-available/000-default.conf

COPY ./docker-entrypoint.sh ./docker-entrypoint.sh
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait

RUN chmod +x /docker-entrypoint.sh && chmod +x /wait

EXPOSE 80
