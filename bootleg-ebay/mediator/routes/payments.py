import os
import requests
import json

from flask_expects_json import expects_json
from flask import Response, request, Blueprint

from utils import get_and_post
from config import *

payments_api = Blueprint('payments', __name__)

# getting IP Address of payments container
# The following are functions for the payments microservice

_payment_info_schema = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'int'},
        'card_number': {'type': 'int'},
        'security_code': {'type': 'int'},
        'expiration_date': {'type': 'string'}
    },
    'required': ['user_id', 'card_number', 'security_code', 'expiration_date']
}

_payment_id_schema = {
    'type': 'object',
    'properties': {
        'payment_id': {'type': 'int'},
    },
    'required': ['payment_id']
}

@payments_api.route("create_payment_card", methods = ['POST'])
@expects_json(_payment_info_schema)
def create_payment_card():
    socket_url = ("http://" + PAYMENTS_SERVICE_HOST + PAYMENTS_PORT + "/create_payment_card")
    return get_and_post(socket_url)

@payments_api.route("get_payment_card", methods = ['POST'])
@expects_json(_payment_id_schema)
def get_payment_card():
    socket_url = ("http://" + PAYMENTS_SERVICE_HOST + PAYMENTS_PORT + "/get_payment_card")
    return get_and_post(socket_url)

@payments_api.route("delete_account", methods = ['POST'])
@expects_json(_payment_id_schema)
def payments_delete_account():
    socket_url = ("http://" + PAYMENTS_SERVICE_HOST + PAYMENTS_PORT + "/delete_account")
    return get_and_post(socket_url)

