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


@payments_api.route("/{}/create_payment_card".format(PAYMENTS_NAME), methods = ['POST'])
def create_payment_card():
    socket_url = ("http://" + PAYMENTS_SERVICE_HOST + PAYMENTS_PORT + "/create_payment_card")
    return get_and_post(socket_url)

@payments_api.route("/{}/get_payment_card".format(PAYMENTS_NAME), methods = ['POST'])
def get_payment_card():
    socket_url = ("http://" + PAYMENTS_SERVICE_HOST + PAYMENTS_PORT + "/get_payment_card")
    return get_and_post(socket_url)

@payments_api.route("/{}/delete_account".format(PAYMENTS_NAME), methods = ['POST'])
def payments_delete_account():
    socket_url = ("http://" + PAYMENTS_SERVICE_HOST + PAYMENTS_PORT + "/delete_account")
    return get_and_post(socket_url)

