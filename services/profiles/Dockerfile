FROM python:3.11.1-slim

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

ADD requirements.txt /requirements.txt

RUN pip install -r /requirements.txt