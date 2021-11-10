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
                            ITEMS_PORT + "/lock")
    available_items = []
    unavailable_items = []
    for item in items:
        availability = (requests.post(url = items_availability_url, data = {"item_id" : item})).content
        if availability == "Was unable to adjust availability. Item is no longer available.":
            unavailable_items.append(item)
        else:
            available_items.append(item)
            
    # GET CREDIT CARD INFO
    user_id = data_content["user_id"]
    socket_url = ("http://" + PAYMENTS_SERVICE_HOST + PAYMENTS_PORT
                    + "/card_by_user/" + user_id)
    r = requests.get(socket_url)
    payment = json.loads(r.content)
    if "error" in payment:
        return "User does not have payment information yet. Please enter your payment information before checking out."
    payment_id = payment["payment_id"]

    # CREATE TRANSACTION INFO
    items_info_url = ("http://" + ITEMS_SERVICE_HOST +
                            ITEMS_PORT + "/get_item")
    transaction_url = ("http://" + PAYMENTS_SERVICE_HOST +
                            PAYMENTS_PORT + "/transaction")

    successfully_bought = []
    for item in available_items:
        item_info = (requests.post(url = items_info_url, data = {"item_id": item})).content
        # for price, I need to figure out whether its an auction or a buy now
        # transaction
        total_price = item_info["price"] + item_info["shipping"]
        transaction = {"user_id": user_id, "payment_id": payment_id, "item_id": item,
                        "money": total_price, "quantity": 1}
        r = requests.post(transaction_url, data = transaction)
        successfully_bought.append(r.content)


    # DELETE ALL ITEMS FROM CART
    empty_cart_url = ("http://" + CARTS_SERVICE_HOST +
                    CARTS_PORT + "/empty_cart")
    r = requests.post(empty_cart_url, data = {"user_id": user_id})

    # return transaction information for successful transactions
    return json.dumps(successfully_bought)



