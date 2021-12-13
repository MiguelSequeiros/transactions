# syntax=docker/dockerfile:1
FROM python:3.6-alpine
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/