FROM python:3.6

ENV PYTHONOUNBUFFERED 1 

WORKDIR /mediator

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
ENV ITEMSAPIHOST=items-api
ENV CARTSAPIHOST=carts-api
ENV USERAPIHOST=users-api
ENV PAYMENTSAPIHOST=payments-api
ENV AUCTIONSAPIHOST=auctions-api
ENV NOTIFSAPIHOST=notifs-api

# CMD ["python", "app.py"]

CMD python app.py & celery -A app.celery worker --loglevel=debug 