import os
import requests
import json

from flask_expects_json import expects_json
from flask import Response, request, Blueprint

from utils import get_and_request
from config import *

payments_api = Blueprint('payments', __name__)

# getting IP Address of payments container
# The following are functions for the payments microservice

_payment_info_schema = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'integer'},
        'card_number': {'type': 'integer'},
        'security_code': {'type': 'integer'},
        'expiration_date': {'type': 'string'}
    },
    'required': ['user_id', 'card_number', 'security_code', 'expiration_date']
}

_payment_id_schema = {
    'type': 'object',
    'properties': {
        'payment_id': {'type': 'integer'},
    },
    'required': ['payment_id']
}

_none_schema = {
    'type': 'object',
    'properties': {
    },
    'required': []
}

@payments_api.route("/card", methods = ['POST'])
@expects_json(_payment_info_schema)
def create_payment_card():
    socket_url = ("http://" + PAYMENTS_SERVICE_HOST + PAYMENTS_PORT + "/card")

    r = get_and_request(socket_url, 'post')
    
    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content

@payments_api.route("/card/<payment_id>", methods = ['GET'])
@expects_json(_none_schema)
def get_payment_card(payment_id):
    socket_url = ("http://" + PAYMENTS_SERVICE_HOST + PAYMENTS_PORT + "/card/{}".format(payment_id))
    r = get_and_request(socket_url, 'get')
    
    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content

@payments_api.route("/card/<payment_id>", methods = ['DELETE'])
@expects_json(_none_schema)
def payments_delete_account(payment_id):
    socket_url = ("http://" + PAYMENTS_SERVICE_HOST + PAYMENTS_PORT + "/card/{}".format(payment_id))
    r = get_and_request(socket_url, 'delete')
    
    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content

