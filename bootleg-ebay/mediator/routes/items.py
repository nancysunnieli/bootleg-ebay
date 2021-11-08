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
        'price': {'type': 'string'}
    },
    'required': ['name', 'description', 'category', 'photos', 'sellerID', 'price']
}

_unrequired_attributes = {
    'type': 'object',
    'properties': {
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
        'category': {'type': 'array'}
    },
    'required': ['category']
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
        'user_id': {'type': 'string'}
    },
    'required': ['user_id']
}


_report = {
    'type': 'object',
    'properties': {
        'reason': {'type': 'string'}
    },
    'required': ['reason']
}

_none_schema = {
    'type': 'object',
    'properties': {
    },
    'required': []
}


@items_api.route('/', methods=['GET'])
def items_service_status():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ITEMS_PORT + "/")
    r = requests.get(url = socket_url)
    if not r.ok:
        return Response(response=r.text, status=r.status_code)
    return r.content


@items_api.route('/all_items', methods=['POST'])
@expects_json(_view_items_schema)
def view_all_items():

    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ITEMS_PORT + "/view_all_items")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content).content

    if not r.ok:
        return Response(response=r.text, status=r.status_code)

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
    r = requests.get(url = socket_url)
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


@items_api.route('/watchlist/<item_id>', methods = ['POST'])
@expects_json(_watchlist)
def add_user_to_watch_list(item_id):
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ITEMS_PORT + "/add_user_to_watch_list")
    data_content = request.get_json()
    user_id = data_content["user_id"]
    r = requests.post(url = socket_url, data = {"item_id": item_id, "user_id": user_id})
    if not r.ok:
        return Response(response=r.text, status=r.status_code)
    return r.content


@items_api.route('/removal/<item_id>', methods = ['POST'])
@expects_json(_none_schema)
def remove_item(item_id):
    socket_url = ("http://" + AUCTIONS_SERVICE_HOST + AUCTIONS_PORT + "/bids")
    r = get_and_request(socket_url, 'get')
    if len(r.content) != 0:
        return """There are already bids on 
                this item! It cannot be deleted"""
    
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ITEMS_PORT + "/remove_item")
    r = requests.post(url = socket_url, data = {"item_id": item_id})
    if not r.ok:
        return Response(response=r.text, status=r.status_code)
    return r.content


@items_api.route('/report/<item_id>', methods = ['POST'])
@expects_json(_report)
def report_item(item_id):
    socket_url = ("http://" + ITEMS_SERVICE_HOST+
                     ITEMS_PORT + "/report_item")
    data_content = request.get_json()
    reason = data_content["reason"]
    r = requests.post(url = socket_url, data = {"reason": reason, "item_id": item_id})
    if not r.ok:
        return Response(response=r.text, status=r.status_code)
    return r.content


@items_api.route("/item/<item_id>", methods = ['POST'])
@expects_json(_none_schema)
def get_item(item_id):
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ITEMS_PORT + "/get_item")
    r = requests.post(url = socket_url, data = {"item_id": item_id})
    if not r.ok:
        return Response(response=r.text, status=r.status_code)
    return r.content


@items_api.route("/modification/<item_id>", methods = ['POST'])
@expects_json(_unrequired_attributes)
def modify_item(item_id):
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ITEMS_PORT + "/modify_item")
    data_content = json.loads(request.get_json())
    data_content["item_id"] = item_id
    r = requests.post(url = socket_url, json = json.dumps(data_content))
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


@items_api.route("/categories/<item_id>", methods = ['POST'])
@expects_json(_category)
def edit_categories(item_id):
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ITEMS_PORT + "/edit_categories")
    data_content = json.loads(request.get_json())
    data_content["item_id"] = item_id
    r = requests.post(url = socket_url, json = json.dumps(data_content))
    if not r.ok:
        return Response(response=r.text, status=r.status_code)
    return r.content


@items_api.route("/availability/<item_id>", methods = ['POST'])
@expects_json(_none_schema)
def modify_availability(item_id):
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ITEMS_PORT + "/modify_availability")
    r = requests.post(url = socket_url, data = {"item_id": item_id})
    if not r.ok:
        return Response(response=r.text, status=r.status_code)
    return r.content