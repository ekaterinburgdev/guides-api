FROM python:3.8.3-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get -y update

RUN apt-get install -y cron && touch /var/log/cron.log

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .