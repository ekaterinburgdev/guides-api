FROM python:3.8.3-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && apt-get -y install libpq-dev gcc

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .