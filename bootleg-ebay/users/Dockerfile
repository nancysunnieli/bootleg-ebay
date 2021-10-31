# syntax=docker/dockerfile:1
FROM ubuntu:20.04
# FROM python:3.7-slim-buster
WORKDIR /bootleg-ebay

RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get --no-install-recommends install -yq \
    build-essential \
    curl \
    git \
    pkg-config \
    python3-dev \
    python3-pip \
    python3-venv

# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
# EXPOSE 5000
# Do not copy because we should mount the volumes instead. See docker-compose
# COPY . .
# CMD ["flask", "run"]

ENV PYTHONOUNBUFFERED 1
ENV USERSDBHOST=users-db
CMD ["python", "app.py"] 