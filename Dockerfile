# pull official base image
FROM python:3.8-alpine
MAINTAINER Rendezvous Code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG 0

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps


RUN mkdir /app
WORKDIR /app
COPY ./app /app

RUN python manage.py collectstatic --noinput

RUN adduser -D user
USER user

# run gunicorn
CMD gunicorn app.wsgi:application --bind 0.0.0.0:$PORT