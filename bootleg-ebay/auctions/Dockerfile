FROM python:3.6
ENV PYTHONOUNBUFFERED 1

COPY ./requirements.txt ./requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r ./requirements.txt

# We've mounted a volume of the application already
WORKDIR /auctions
ENV AUCTIONSDBHOST=auctions-db
ENV AUCTIONSDBPORT=27017
CMD ["python", "app.py"] 