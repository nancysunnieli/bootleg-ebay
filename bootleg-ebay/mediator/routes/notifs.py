import requests
import os
import requests
import json

from flask_expects_json import expects_json
from flask import Response, request, Blueprint

from utils import get_and_request
from config import *

# getting IP Address of items container
# The following functions call the notifications microservice

notifs_api = Blueprint('notifs', __name__)



EmailPostSchema = {
    'type': 'object',
    'properties': {
        'recipient': {'type': 'string',  "minLength": 1},
        'subject': {'type': 'string'},
        'body': {'type': 'string'},
    },
    'required': ['recipient', 'subject', 'body']
}

RecipientAuction= {
    'type': 'object',
    'properties': {
        'recipient' : {'type': 'string'},
        'auction_id' : {'type' : 'string'},
    },
    'required': ['recipient', 'auction_id']
}

Time= {
    'type': 'object',
    'properties': {
        'recipient' : {'type': 'string'},
        'auction_id' : {'type' : 'string'},
        'time_left' : {'type' : 'string'},
    },
    'required': ['recipient', 'auction_id', 'time_left']
}

@notifs_api.route('/', methods=['GET'])
def notifs_service_status():
    socket_url = ("http://" + NOTIFS_SERVICE_HOST +
                     NOTIFS_PORT + "/")
    r = requests.get(url = socket_url)
    if not r.ok:
        return Response(response=r.text, status=r.status_code)
    return r.content


@notifs_api.route('/email', methods = ['POST'])
@expects_json(EmailPostSchema)
def email():
    socket_url = ("http://" + NOTIFS_SERVICE_HOST +
                    NOTIFS_PORT + "/email")
    data = request.get_json()
    r = requests.post(url = socket_url, json = data)
    if not r.ok:
        return Response(response=r.text, status=r.status_code)
    return r.content  

@notifs_api.route('/watchlist', methods = ['POST'])
@expects_json(RecipientAuction)
def watchlist():
    socket_url = ("http://" + NOTIFS_SERVICE_HOST +
                    NOTIFS_PORT + "/watchlist")
    data = request.get_json()
    r = requests.post(url = socket_url, json = data)
    if not r.ok:
        return Response(response=r.text, status=r.status_code)
    return r.content    

@notifs_api.route('/seller_bid', methods = ['POST'])
@expects_json(RecipientAuction)
def alert_seller():
    socket_url = ("http://" + NOTIFS_SERVICE_HOST +
                    NOTIFS_PORT + "/seller_bid")
    data = request.get_json()
    r = requests.post(url = socket_url, json = data)
    if not r.ok:
        return Response(response=r.text, status=r.status_code)
    return r.content

@notifs_api.route('/buyer_bid', methods = ['POST'])
@expects_json(RecipientAuction)
def alert_buyer():
    socket_url = ("http://" + NOTIFS_SERVICE_HOST +
                    NOTIFS_PORT + "/buyer_bid")
    data = request.get_json()
    r = requests.post(url = socket_url, json = data)
    if not r.ok:
        return Response(response=r.text, status=r.status_code)
    return r.content

@notifs_api.route('/time', methods = ['POST'])
@expects_json(Time)
def time():
    socket_url = ("http://" + NOTIFS_SERVICE_HOST +
                    NOTIFS_PORT + "/time")
    data = request.get_json()
    r = requests.post(url = socket_url, json = data)
    if not r.ok:
        return Response(response=r.text, status=r.status_code)
    return r.content   

@notifs_api.route('/inbox', methods = ['GET'])
def inbox():
    socket_url = ("http://" + NOTIFS_SERVICE_HOST +
                    NOTIFS_PORT + "/inbox")
    r = requests.get(url = socket_url)
    if not r.ok:
        return Response(response=r.text, status=r.status_code)
    return r.content




