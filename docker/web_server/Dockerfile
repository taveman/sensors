FROM python:3.7-alpine
MAINTAINER Yuiry

ENV PYTHONUNBUFFERED 1

COPY /requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

RUN mkdir /web_app
WORKDIR /web_app

COPY ["/", "/web_app"]

RUN adduser -D web_user
RUN mkdir /var/log/web
RUN chown web_user:web_user /var/log/web
USER web_user