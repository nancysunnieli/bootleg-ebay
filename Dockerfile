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


FROM python:3.6
ENV PYTHONOUNBUFFERED 1
WORKDIR /bootleg-ebay
COPY ./bootleg-ebay/items/app.py ./items/app.py
COPY ./bootleg-ebay/items/item_functions.py ./items/item_functions.py
COPY ./bootleg-ebay/mediator/app.py ./mediator/app.py
CMD ["python", "./items/app.py"]
CMD ["python", "./mediator/app.py"]

COPY requirements.txt ./requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# ENV FLASK_APP=app.py
# ENV FLASK_RUN_HOST=0.0.0.0
# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt
# EXPOSE 5000
# Do not copy because we should mount the volumes instead. See docker-compose
# COPY . .
# CMD ["flask", "run"]