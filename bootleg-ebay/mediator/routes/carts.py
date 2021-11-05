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

_user = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'string'}
    },
    'required': ['user_id']
}

_user_item = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'string'},
        'item_id': {'type': 'string'}
    },
    'required': ['user_id', 'item_id']
}


@carts_api.route("/create_cart", methods = ['POST'])
@expects_json(_user)
def create_cart():
    socket_url = ("http://" + CARTS_SERVICE_HOST +
                    CARTS_PORT + "/create_cart")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@carts_api.route("/add_item_to_cart", methods = ['POST'])
@expects_json(_user_item)
def add_item_to_cart():
    socket_url = ("http://" + CARTS_SERVICE_HOST +
                    CARTS_PORT + "/add_item_to_cart")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@carts_api.route("/delete_item_from_cart", methods = ['POST'])
@expects_json(_user_item)
def delete_item_from_cart():
    socket_url = ("http://" + CARTS_SERVICE_HOST +
                    CARTS_PORT + "/delete_item_from_cart")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@carts_api.route("/get_items_from_cart", methods = ['POST'])
@expects_json(_user)
def get_items_from_cart():
    socket_url = ("http://" + CARTS_SERVICE_HOST +
                    CARTS_PORT + "/get_items_from_cart")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@carts_api.route("/empty_cart", methods = ['POST'])
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
    data_content = request.get_json()

    # gets all items in user's cart
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
    r = requests.post(empty_cart_url, json = data_content)
    return r.content



