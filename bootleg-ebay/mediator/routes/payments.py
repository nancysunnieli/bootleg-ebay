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


@routes.route("/{}/CreatePaymentCard".format(paymentsName), methods = ['POST'])
def CreatePaymentCard():
    socket_url = ("http://" + paymentsServiceHost + paymentsPort + "/CreatePaymentCard")
    return get_and_post(socket_url)

@routes.route("/{}/GetPaymentCard".format(paymentsName), methods = ['POST'])
def GetPaymentCard():
    socket_url = ("http://" + paymentsServiceHost + paymentsPort + "/GetPaymentCard")
    return get_and_post(socket_url)

@routes.route("/{}/DeleteAccount".format(paymentsName), methods = ['POST'])
def PaymentsDeleteAccount():
    socket_url = ("http://" + paymentsServiceHost + paymentsPort + "/DeleteAccount")
    return get_and_post(socket_url)

