import os
import requests
import json

from flask_expects_json import expects_json
from flask import Response, request, Blueprint

from utils import get_and_post
from config import *
import time

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

@carts_api.route("/removal", methods = ['POST'])
@expects_json(_item)
def delete_item_from_cart():
    socket_url = ("http://" + CARTS_SERVICE_HOST +
                    CARTS_PORT + "/delete_item_from_cart")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
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
    items = requests.post(url = get_items_url, json = data_content).content

    items = json.loads(items)
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

    # get user_id from username
    username = data_content["user_id"]
    
    user_id_url = ("http://" + USERS_SERVICE_HOST +
                    USERS_PORT + "/user_by_name/" + username)
    user_id = json.loads(requests.get(url = user_id_url).content)
    user_id = user_id["user_id"]


    # GET CREDIT CARD INFO
    socket_url = ("http://" + PAYMENTS_SERVICE_HOST + PAYMENTS_PORT
                    + "/card_by_user/" + str(user_id))
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

    # getting current time to compare with auction end times
    current_time = int(time.time())
    successfully_bought = []
    seen_auctions = []
    for item in available_items:
        item_info = requests.post(url = items_info_url, json = json.dumps({"item_id": item})).content
        item_info = json.loads(item_info)
        # for price, I need to figure out whether its an auction or a buy now
        # transaction

        # I have to call get auction by item id
        auction_url = ("http://" + AUCTIONS_SERVICE_HOST +
                            AUCTIONS_PORT + "/auctions_by_item/" + item)
        auctions = json.loads(requests.get(auction_url).content)
        
        total_price = None
        for auction in auctions:
            if auction["auction_id"] not in seen_auctions:
                if auction["end_time"] < current_time:
                    most_recent_bid_time = 0
                    most_recent_buyer = None
                    most_recent_price = None
                    for bid in auction["bids"]:
                        if bid["bid_time"] > most_recent_bid_time:
                            most_recent_bid_time = bid["bid_time"]
                            most_recent_buyer = bid["buyer_id"]
                            most_recent_price = bid["price"]
                    if most_recent_buyer == username:
                        seen_auctions.append(auction["auction_id"])
                        total_price = item_info["shipping"] + most_recent_price
                        break

        if not total_price:
            total_price = float(item_info["price"]) + float(item_info["shipping"])

        transaction = {"user_id": user_id, "payment_id": payment_id, "item_id": item,
                        "money": total_price, "quantity": 1}
        transaction = json.dumps(transaction)

        r = requests.post(transaction_url, json = transaction)

        successfully_bought.append(json.loads(r.content))

    # DELETE ALL ITEMS FROM CART
    empty_cart_url = ("http://" + CARTS_SERVICE_HOST +
                    CARTS_PORT + "/empty_cart")
    r = requests.post(empty_cart_url, json = json.dumps({"user_id": username}))

    # return transaction information for successful transactions
    return json.dumps(successfully_bought)



