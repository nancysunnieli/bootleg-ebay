# syntax=docker/dockerfile:1
FROM ubuntu:20.04

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

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENV PYTHONOUNBUFFERED 1
ENV AUCTIONSDBHOST=auctions-db
CMD ["python3", "app.py"] 