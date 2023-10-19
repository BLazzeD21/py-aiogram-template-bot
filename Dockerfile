FROM python:3.11.6-slim-bullseye

RUN apt-get update && apt-get install -y redis-server

COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app
WORKDIR /app

CMD service redis-server start && python3 start.py