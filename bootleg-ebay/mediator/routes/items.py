import requests
import os
import requests
import json

from flask_expects_json import expects_json
from flask import Response, request, Blueprint

from utils import get_and_post
from config import *
from .auctions import view_bids, view_current_auctions


# getting IP Address of items container
# The following functions call the items microservice

items_api = Blueprint('items', __name__)

_required_attributes = {
    'type': 'object',
    'properties': {
        'item_id': {'type': 'string'},
        'name': {'type': 'string'},
        'description' : {'type' : 'string'},
        'category': {'type': 'string'},
        'photos': {'type': 'string'},
        'sellerID': {'type': 'string'},
        'price': {'type': 'string'}
    },
    'required': ['item_id', 'name', 'description', 'category', 'photos', 'sellerID', 'price']
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
        'price': {'type': 'string'}
    },
    'required': []
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
        'limit' : {'type': 'int'}
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
        'user_id': {'type': 'string'}
    },
    'required': ['item_id', 'user_id']
}

_item = {
    'type': 'object',
    'properties': {
        'item_id' : {'type': 'string'}
    },
    'required': ['item_id']
}

_report = {
    'type': 'object',
    'properties': {
        'item_id' : {'type': 'string'},
        'reason': {'type': 'string'}
    },
    'required': ['item_id', 'reason']
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
    current_auctions = json.loads(view_current_auctions())
    available = set()
    for auction in current_auctions:
        available.add(auction["item_id"])

    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ITEMS_PORT + "/view_all_items")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content).content

    all_items = []
    for item in json.loads(r):
        if item["_id"] in available:
            del item["_id"]
            all_items.append(item)
    return json.dumps(all_items)

@items_api.route('/flagged_items', methods=['POST'])
@expects_json(_view_items_schema)
def view_flagged_items():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ITEMS_PORT + "/view_flagged_items")
    r = requests.get(url = socket_url)
    return r.content


@items_api.route('/search', methods=['POST'])
@expects_json(_search_items)
def search_item():
    socket_url = ("http://" +ITEMS_SERVICE_HOST +
                     ITEMS_PORT + "/search_item")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@items_api.route('/watch_list_addition', methods = ['POST'])
@expects_json(_watchlist)
def add_user_to_watch_list():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ITEMS_PORT + "/add_user_to_watch_list")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content



@items_api.route('/removal', methods = ['POST'])
@expects_json(_item)
def remove_item():
    if view_bids().length == 0:
        return """There are already bids on 
                this item! It cannot be deleted"""
    
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ITEMS_PORT + "/remove_item")
    data_content = request.get_json()
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
@expects_json(_item)
def get_item():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ITEMS_PORT + "/get_item")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@items_api.route("/item_updates", methods = ['POST'])
@expects_json(_unrequired_attributes)
def modify_item():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ITEMS_PORT + "/modify_item")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@items_api.route("/item_additions", methods = ['POST'])
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
@expects_json(_item)
def modify_availability():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ITEMS_PORT + "/modify_availability")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content