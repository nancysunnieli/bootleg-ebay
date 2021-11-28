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
        'user_id': {'type': 'number'}
    },
    'required': ['item_id', 'user_id']
}

_user = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'number'}
    },
    'required': ['user_id']
}

@carts_api.route("/remove_cart", methods = ['POST'])
@expects_json(_user)
def remove_cart():
    socket_url = ("http://" + CARTS_SERVICE_HOST +
                    CARTS_PORT + "/remove_cart")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    if not r.ok:
        return Response(response=r.text, status=r.status_code)
    return r.content

@carts_api.route("/cart", methods = ['POST'])
@expects_json(_user)
def create_cart():
    socket_url = ("http://" + CARTS_SERVICE_HOST +
                    CARTS_PORT + "/create_cart")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    if not r.ok:
        return Response(response=r.text, status=r.status_code)
    return r.content

@carts_api.route("/addition", methods = ['POST'])
@expects_json(_item)
def add_item_to_cart():
    socket_url = ("http://" + CARTS_SERVICE_HOST +
                    CARTS_PORT + "/add_item_to_cart")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    if not r.ok:
        return Response(response=r.text, status=r.status_code)
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

@carts_api.route("/cart/<user_id>", methods = ['GET'])
def get_items_from_cart(user_id):
    socket_url = ("http://" + CARTS_SERVICE_HOST +
                    CARTS_PORT + "/get_items_from_cart")
    data_content = {"user_id": int(user_id)}
    r = requests.post(url = socket_url, json = data_content)
    if not r.ok:
        return Response(response=r.text, status=r.status_code)
    # getting actual items from item_ids
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ITEMS_PORT + "/get_item")
    all_items = []
    seen_auctions = []
    for item_id in json.loads(r.content):
        data_content = {"item_id": item_id}
        r = requests.post(url = socket_url, json = json.dumps(data_content))
        if not r.ok:
            return Response(response=r.text, status=r.status_code)
        item = json.loads(r.content)
        
        auction_url = ("http://" + AUCTIONS_SERVICE_HOST +
                     AUCTIONS_PORT + "/auctions_by_item/" + item_id)
        r = requests.get(url=auction_url)
        if not r.ok:
            return Response(response=r.text, status=r.status_code)
        
        item_price = None
        shipping_price = None
        

        current_time = time.time()
        auctions = json.loads(r.content)
        for auction in auctions:
            if auction["end_time"] < current_time:
                if auction["auction_id"] not in seen_auctions:
                    most_recent_bid_time = 0
                    most_recent_buyer = None
                    most_recent_price = None
                    for bid in auction["bids"]:
                        if bid["bid_time"] > most_recent_bid_time:
                            most_recent_bid_time = bid["bid_time"]
                            most_recent_buyer = bid["buyer_id"]
                            most_recent_price = bid["price"]
                        if most_recent_buyer == user_id:
                            seen_auctions.append(auction["auction_id"])
                            shipping_price = auction["shipping"]
                            item_price = most_recent_price
                            break

        if not item_price:
            for auction in auctions:
                if auction["end_time"] >= current_time and auction["start_time"] <= current_time:
                    price = float(auction["buy_now_price"]) + float(auction["shipping"])
                    item_price = auction["buy_now_price"]
                    shipping_price = auction["shipping"]
                    break
        
        # note, if the price is still null, this means that we cannot buy the item,
        # but this doesn't really matter, because we don't allow for check out.

        item["item_price"] = item_price
        item["shipping_price"] = shipping_price
        all_items.append(item)

    return json.dumps(all_items)

@carts_api.route("/empty", methods = ['POST'])
@expects_json(_user)
def empty_cart():
    socket_url = ("http://" + CARTS_SERVICE_HOST +
                    CARTS_PORT + "/empty_cart")
    data_content = request.get_json()
    r = requests.post(socket_url, json = data_content)
    if not r.ok:
        return Response(response=r.text, status=r.status_code)
    return r.content

@carts_api.route("/checkout", methods = ['POST'])
@expects_json(_user)
def checkout():
    # gets all items in user's cart
    data_content = request.get_json()
    get_items_url = ("http://" + CARTS_SERVICE_HOST +
                    CARTS_PORT + "/get_items_from_cart")
    r = requests.post(url = get_items_url, json = data_content)
    if not r.ok:
        return Response(response=r.text, status=r.status_code)
    items = r.content

    items = json.loads(items)
    # checks availability of all items
    items_availability_url = ("http://" + ITEMS_SERVICE_HOST +
                            ITEMS_PORT + "/lock")
    available_items = []
    unavailable_items = []
    for item in items:
        item_dict = {"item_id" : item}
        r = requests.post(url = items_availability_url, json = item_dict)
        if not r.ok:
            unavailable_items.append(item)
        else:
            available_items.append(item)
    # get user_id from username
    user_id = data_content["user_id"]


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
    current_time = time.time()
    successfully_bought = []
    seen_auctions = []
    for item in available_items:
        r = requests.post(url = items_info_url, json = json.dumps({"item_id": item}))
        if not r.ok:
            return Response(response=r.text, status=r.status_code)
        item_info = r.content
        item_info = json.loads(item_info)
        # for price, I need to figure out whether its an auction or a buy now
        # transaction

        # I have to call get auction by item id
        auction_url = ("http://" + AUCTIONS_SERVICE_HOST +
                            AUCTIONS_PORT + "/auctions_by_item/" + item)
        r = requests.get(auction_url)
        if not r.ok:
            return Response(response=r.text, status=r.status_code)
        auctions = json.loads(r.content)
        
        total_price = None
        for auction in auctions:
            if auction["auction_id"] not in seen_auctions:
                if auction["completed"] == False:
                    if auction["end_time"] < current_time:
                        most_recent_bid_time = 0
                        most_recent_buyer = None
                        most_recent_price = None
                        for bid in auction["bids"]:
                            if bid["bid_time"] > most_recent_bid_time:
                                most_recent_bid_time = bid["bid_time"]
                                most_recent_buyer = bid["buyer_id"]
                                most_recent_price = bid["price"]
                        if most_recent_buyer == user_id:
                            seen_auctions.append(auction["auction_id"])
                            total_price = auction["shipping"] + most_recent_price


                            auction_url = ("http://" + AUCTIONS_SERVICE_HOST +
                            AUCTIONS_PORT + "/auction/" + auction["auction_id"])
                            r = requests.post(url = auction_url, json = {"completed": True})
                            if not r.ok:
                                return Response(response=r.text, status=r.status_code)
                            break

        if not total_price:
            # also have to complete current auctions
            for auction in auctions:

                if auction["end_time"] >= current_time and auction["start_time"] <= current_time:
                    total_price = float(auction["buy_now_price"]) + float(auction["shipping"])
                    auction_url = ("http://" + AUCTIONS_SERVICE_HOST +
                            AUCTIONS_PORT + "/auction/" + auction["auction_id"])
                    r = requests.post(url = auction_url, json = {"completed": True})
                    if not r.ok:
                        return Response(response=r.text, status=r.status_code)
                    break

        transaction = {"user_id": user_id, "payment_id": payment_id, "item_id": item,
                        "money": total_price, "quantity": 1}

        r = requests.post(transaction_url, json = transaction)
        if not r.ok:
            return Response(response=r.text, status=r.status_code)

        successfully_bought.append(json.loads(r.content))



    # DELETE ALL ITEMS FROM CART
    empty_cart_url = ("http://" + CARTS_SERVICE_HOST +
                    CARTS_PORT + "/empty_cart")
    user = {"user_id": user_id}

    r = requests.post(empty_cart_url, json = user)
    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    # return transaction information for successful transactions
    return json.dumps(successfully_bought)



