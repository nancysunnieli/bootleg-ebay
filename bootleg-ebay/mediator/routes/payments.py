import os
import requests
import json

from flask_expects_json import expects_json
from flask import Response, request

from utils import get_and_post
from . import routes
from config import *

# getting IP Address of payments container
# The following are functions for the payments microservice


@routes.route("/{}/CreatePaymentCard".format(PAYMENTS_NAME), methods = ['POST'])
def CreatePaymentCard():
    socket_url = ("http://" + PAYMENTS_SERVICE_HOST + PAYMENTS_PORT + "/CreatePaymentCard")
    return get_and_post(socket_url)

@routes.route("/{}/GetPaymentCard".format(PAYMENTS_NAME), methods = ['POST'])
def GetPaymentCard():
    socket_url = ("http://" + PAYMENTS_SERVICE_HOST + PAYMENTS_PORT + "/GetPaymentCard")
    return get_and_post(socket_url)

@routes.route("/{}/delete_account".format(PAYMENTS_NAME), methods = ['POST'])
def PaymentsDeleteAccount():
    socket_url = ("http://" + PAYMENTS_SERVICE_HOST + PAYMENTS_PORT + "/delete_account")
    return get_and_post(socket_url)

