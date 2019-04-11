FROM python:3.7-alpine
MAINTAINER Yuiry

ENV PYTHONUNBUFFERED 1

COPY /requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

RUN mkdir /sensor_app
WORKDIR /sensor_app

COPY ["/", "/sensor_app"]

RUN adduser -D sensor_user
RUN mkdir /var/log/sensor
RUN chown sensor_user:sensor_user /var/log/sensor
USER sensor_user