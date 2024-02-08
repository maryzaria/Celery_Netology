FROM python:3.10-alpine3.16

ENV PYTHONUNBUFFERED 1

COPY ./ /app

WORKDIR /app

RUN pip install -r /app/requirements.txt