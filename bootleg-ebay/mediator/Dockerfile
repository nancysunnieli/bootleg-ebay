FROM python:3.6

ENV PYTHONOUNBUFFERED 1 

WORKDIR /mediator

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
ENV ITEMSAPIHOST=items-api
ENV CARTSAPIHOST=carts-api

CMD ["python", "app.py"]