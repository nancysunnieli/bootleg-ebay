import os
import requests
import json

from flask_expects_json import expects_json
from flask import Response, request, Blueprint

from utils import get_and_post
from config import *

# getting IP Address of carts container
# The following are functions for the carts microservice

carts_api = Blueprint('carts', __name__)


_none_schema = {
    'type': 'object',
    'properties': {
    },
    'required': []
}

_item = {
    'type': 'object',
    'properties': {
        'item_id': {'type': 'string'},
        'user_id': {'type': 'string'}
    },
    'required': ['item_id', 'user_id']
}

_user = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'string'}
    },
    'required': ['user_id']
}


@carts_api.route("/creation", methods = ['POST'])
@expects_json(_user)
def create_cart():
    socket_url = ("http://" + CARTS_SERVICE_HOST +
                    CARTS_PORT + "/create_cart")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@carts_api.route("/addition", methods = ['POST'])
@expects_json(_item)
def add_item_to_cart():
    socket_url = ("http://" + CARTS_SERVICE_HOST +
                    CARTS_PORT + "/add_item_to_cart")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@carts_api.route("/removal/<user_id>", methods = ['POST'])
@expects_json(_item)
def delete_item_from_cart(user_id):
    socket_url = ("http://" + CARTS_SERVICE_HOST +
                    CARTS_PORT + "/delete_item_from_cart")
    data_content = json.loads(request.get_json())
    data_content["user_id"] = user_id
    r = requests.post(url = socket_url, data = json.dumps(data_content))
    if not r.ok:
        return Response(response=r.text, status=r.status_code)
    return r.content

@carts_api.route("/cart", methods = ['POST'])
@expects_json(_user)
def get_items_from_cart():
    socket_url = ("http://" + CARTS_SERVICE_HOST +
                    CARTS_PORT + "/get_items_from_cart")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@carts_api.route("/empty", methods = ['POST'])
@expects_json(_user)
def empty_cart():
    socket_url = ("http://" + CARTS_SERVICE_HOST +
                    CARTS_PORT + "/empty_cart")
    data_content = request.get_json()
    r = requests.post(socket_url, json = data_content)
    return r.content

@carts_api.route("/checkout", methods = ['POST'])
@expects_json(_user)
def checkout():
    # gets all items in user's cart
    data_content = request.get_json()
    get_items_url = ("http://" + CARTS_SERVICE_HOST +
                    CARTS_PORT + "/get_items_from_cart")
    items = json.loads((requests.post(url = get_items_url, json = data_content)).content)


    # checks availability of all items
    items_availability_url = ("http://" + ITEMS_SERVICE_HOST +
                            ":8099" + "/get_items_from_cart")
    available_items = []
    unavailable_items = []
    for item in items:
        availability = (requests.post(url = items_availability_url, data = {"item_id" : item})).content
        if availability == "Was unable to adjust availability. Item is no longer available.":
            unavailable_items.append(item)
        else:
            available_items.append(item)
    
    # GET CREDIT CARD INFO
    

    # CREATE PAYMENT INFO




    # DELETE ALL ITEMS FROM CART
    empty_cart_url = ("http://" + CARTS_SERVICE_HOST +
                    CARTS_PORT + "/empty_cart")
    r = requests.post(empty_cart_url, data = {"user_id": user_id})
    return r.content



