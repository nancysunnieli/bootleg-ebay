import requests
import os
import requests
import json

from flask_expects_json import expects_json
from flask import Response, request, Blueprint

from utils import get_and_request
from config import *


# getting IP Address of items container
# The following functions call the items microservice

items_api = Blueprint('items', __name__)

_required_attributes = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'description' : {'type' : 'string'},
        'category': {'type': 'array'},
        'photos': {'type': 'string'},
        'sellerID': {'type': 'number'},
        'quantity': {'type': 'number'}
    },
    'required': ['name', 'description', 'category', 'photos', 'sellerID', 'quantity']
}

_unrequired_attributes = {
    'type': 'object',
    'properties': {
        'item_id': {'type': 'string'},
        'name': {'type': 'string'},
        'description' : {'type' : 'string'},
        'category': {'type': 'array'},
        'photos': {'type': 'string'},
        'sellerID': {'type': 'number'},
        'quantity': {'type': 'number'}
    },
    'required': ['item_id']
}

_category = {
    'type': 'object',
    'properties': {
        'item_id': {'type': 'string'},
        'category': {'type': 'array'}
    },
    'required': ['item_id', 'category']
}

_view_items_schema = {
    'type': 'object',
    'properties': {
        'limit' : {'type': 'number'}
    },
    'required': []
}

_search_items = {
    'type': 'object',
    'properties': {
        'keywords' : {'type': 'array'},
        'category' : {'type': 'string'}
    },
    'required': []
}

_watchlist = {
    'type': 'object',
    'properties': {
        'item_id': {'type': 'string'},
        'user_id': {'type': 'number'},
        'max_price': {'type': 'number'}
    },
    'required': ['user_id', 'item_id', 'max_price']
}


_report = {
    'type': 'object',
    'properties': {
        'item_id': {'type': 'string'},
        'reason': {'type': 'string'}
    },
    'required': ['item_id', 'reason']
}

_none_schema = {
    'type': 'object',
    'properties': {
    },
    'required': []
}

_item_schema = {
    'type': 'object',
    'properties': {
        'item_id': {'type': 'string'},
    },
    'required': ['item_id']
}

_category_only = {
    'type': 'object',
    'properties': {
        'category': {'type': 'string'},
    },
    'required': ['category']
}


@items_api.route('/', methods=['GET'])
def items_service_status():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ITEMS_PORT + "/")
    r = requests.get(url = socket_url)
    return r.content


@items_api.route('/all_items', methods=['POST'])
@expects_json(_view_items_schema)
def view_all_items():

    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ITEMS_PORT + "/view_all_items")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)

    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    all_items = []
    for item in json.loads(r.content):
        all_items.append(item)
    return json.dumps(all_items)

@items_api.route('/flagged_items', methods=['POST'])
@expects_json(_view_items_schema)
def view_flagged_items():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ITEMS_PORT + "/view_flagged_items")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)

    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content


@items_api.route('/search', methods=['POST'])
@expects_json(_search_items)
def search_item():
    socket_url = ("http://" +ITEMS_SERVICE_HOST +
                     ITEMS_PORT + "/search_item")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)

    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content


@items_api.route('/watchlist', methods = ['POST'])
@expects_json(_watchlist)
def add_user_to_watch_list():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ITEMS_PORT + "/add_user_to_watch_list")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)

    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content


@items_api.route('/removal', methods = ['POST'])
@expects_json(_item_schema)
def remove_item():
    
    # getting auction name
    # commenting this out until auctions starts running
    
    data_content = request.get_json()
    item_id = data_content["item_id"]
    socket_url = ("http://" + AUCTIONS_SERVICE_HOST + AUCTIONS_PORT + "/current_auctions")
    r = get_and_request(socket_url, 'get')
    auction_id = None
    for auction in json.loads(r.content):
        if auction["item_id"] == item_id:
            auction_id = auction["auction_id"]
    
    if auction_id:
        socket_url = ("http://" + AUCTIONS_SERVICE_HOST + AUCTIONS_PORT + "/bids")
        r = get_and_request(socket_url, 'get')
        if len(r.content) != 0:
            return "There are already bids on this item! It cannot be deleted"

    data_content = request.get_json()
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ITEMS_PORT + "/remove_item")
    
    r = requests.post(url = socket_url, json = data_content)

    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    # remove all associated auctions
    socket_url = ("http://" + AUCTIONS_SERVICE_HOST +
                     AUCTIONS_PORT + "/auctions_by_item/" + item_id)
    auctions = json.loads(requests.get(url = socket_url).content)

    
    for auction in auctions:
        socket_url = ("http://" + AUCTIONS_SERVICE_HOST +
                     AUCTIONS_PORT + "/auction/" + auction["auction_id"])
        remove_auction = requests.delete(url=socket_url)

    return r.content


@items_api.route('/report', methods = ['POST'])
@expects_json(_report)
def report_item():
    socket_url = ("http://" + ITEMS_SERVICE_HOST+
                     ITEMS_PORT + "/report_item")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)

    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content


@items_api.route("/item", methods = ['POST'])
@expects_json(_item_schema)
def get_item():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ITEMS_PORT + "/get_item")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = json.dumps(data_content))

    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content


@items_api.route("/modification", methods = ['POST'])
@expects_json(_unrequired_attributes)
def modify_item():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ITEMS_PORT + "/modify_item")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)

    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content


@items_api.route("/addition", methods = ['POST'])
@expects_json(_required_attributes)
def add_item():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ITEMS_PORT + "/add_item")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)

    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content


@items_api.route("/categories", methods = ['POST'])
@expects_json(_category)
def edit_categories():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ITEMS_PORT + "/edit_categories")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)

    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content


@items_api.route("/lock", methods = ['POST'])
@expects_json(_item_schema)
def modify_quantity():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ITEMS_PORT + "/lock")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)

    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content


@items_api.route("/all_categories", methods = ['GET'])
def get_categories():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ITEMS_PORT + "/categories")
    r = requests.get(url = socket_url)

    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content


@items_api.route("/category_addition", methods = ['POST'])
@expects_json(_category_only)
def add_category():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ITEMS_PORT + "/add_category")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)

    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content

@items_api.route("/category_removal", methods = ['POST'])
@expects_json(_category_only)
def remove_category():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ITEMS_PORT + "/remove_category")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)

    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content


@items_api.route("/items_by_seller/<seller_id>", methods = ['GET'])
def items_by_seller(seller_id):
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ITEMS_PORT + "/items_by_seller")
    data_content = {"sellerID": seller_id}
    r = requests.post(url = socket_url, json = data_content)

    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content

