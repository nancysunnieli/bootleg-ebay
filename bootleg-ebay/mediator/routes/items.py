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
        'category': {'type': 'string'},
        'photos': {'type': 'string'},
        'sellerID': {'type': 'string'},
        'price': {'type': 'number'}
    },
    'required': ['name', 'description', 'category', 'photos', 'sellerID', 'price']
}

_unrequired_attributes = {
    'type': 'object',
    'properties': {
        'item_id': {'type': 'string'},
        'name': {'type': 'string'},
        'description' : {'type' : 'string'},
        'category': {'type': 'string'},
        'photos': {'type': 'string'},
        'sellerID': {'type': 'string'},
        'price': {'type': 'number'}
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
        'keywords' : {'type': 'array'}
    },
    'required': ['keywords']
}

_watchlist = {
    'type': 'object',
    'properties': {
        'item_id': {'type': 'string'},
        'user_id': {'type': 'string'},
    },
    'required': ['user_id', 'item_id']
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
    r = requests.post(url = socket_url, json = data_content).content

    all_items = []
    for item in json.loads(r):
        del item["_id"]
        all_items.append(item)
    return json.dumps(all_items)

@items_api.route('/flagged_items', methods=['POST'])
@expects_json(_view_items_schema)
def view_flagged_items():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ITEMS_PORT + "/view_flagged_items")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@items_api.route('/search', methods=['POST'])
@expects_json(_search_items)
def search_item():
    socket_url = ("http://" +ITEMS_SERVICE_HOST +
                     ITEMS_PORT + "/search_item")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@items_api.route('/watchlist', methods = ['POST'])
@expects_json(_watchlist)
def add_user_to_watch_list():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ITEMS_PORT + "/add_user_to_watch_list")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@items_api.route('/removal', methods = ['POST'])
@expects_json(_item_schema)
def remove_item():
    """
    # getting auction name
    data_content = request.get_json()
    socket_url = ("http://" + AUCTIONS_SERVICE_HOST + AUCTIONS_PORT + "/current_auctions")
    r = get_and_request(socket_url, 'get')

    auction_id = None
    for auction in r.content:
        if auction["item_id"] == json.loads(data_content)["item_id"]:
            auction_id = auction["_id"]

    if auction_id:
        # auctions isn't working
        socket_url = ("http://" + AUCTIONS_SERVICE_HOST + AUCTIONS_PORT + "/bids")
        r = get_and_request(socket_url, 'get')
        return r.content
        if len(r.content) != 0:
            return "There are already bids on this item! It cannot be deleted"
    """
    data_content = request.get_json()
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ITEMS_PORT + "/remove_item")
    
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@items_api.route('/report', methods = ['POST'])
@expects_json(_report)
def report_item():
    socket_url = ("http://" + ITEMS_SERVICE_HOST+
                     ITEMS_PORT + "/report_item")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@items_api.route("/item", methods = ['POST'])
@expects_json(_item_schema)
def get_item():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ITEMS_PORT + "/get_item")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@items_api.route("/modification", methods = ['POST'])
@expects_json(_unrequired_attributes)
def modify_item():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ITEMS_PORT + "/modify_item")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@items_api.route("/addition", methods = ['POST'])
@expects_json(_required_attributes)
def add_item():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ITEMS_PORT + "/add_item")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@items_api.route("/categories", methods = ['POST'])
@expects_json(_category)
def edit_categories():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ITEMS_PORT + "/edit_categories")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@items_api.route("/availability", methods = ['POST'])
@expects_json(_item_schema)
def modify_availability():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ITEMS_PORT + "/modify_availability")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content