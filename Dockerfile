FROM python:3.11.0-slim-bullseye

ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install -y apache2 apache2-dev apache2-utils python3-dev libpq-dev build-essential

RUN pip install mod_wsgi
RUN mod_wsgi-express install-module > /etc/apache2/mods-available/wsgi.load

RUN a2enmod wsgi
# RUN a2enmod ssl

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt
RUN pip install psycopg2

COPY ./deinplugin /var/www/deinplugin
COPY ./apache-config.conf /etc/apache2/sites-available/000-default.conf

COPY ./docker-entrypoint.sh ./docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait

EXPOSE 80
