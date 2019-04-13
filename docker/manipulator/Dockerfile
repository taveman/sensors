FROM python:3.7-alpine
MAINTAINER Yuiry

ENV PYTHONUNBUFFERED 1

COPY /requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

RUN mkdir /manipulator_app
WORKDIR /manipulator_app

COPY ["/", "/manipulator_app"]

RUN adduser -D manipulator_user
RUN mkdir /var/log/manipulator
RUN chown manipulator_user:manipulator_user /var/log/manipulator
USER manipulator_user