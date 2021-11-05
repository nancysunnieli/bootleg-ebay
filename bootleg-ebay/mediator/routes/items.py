import requests
import os
import requests
import json

from flask_expects_json import expects_json
from flask import Response, request, Blueprint

from utils import get_and_post
from config import *


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
    }
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

def ItemsServiceStatus():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ITEMS_PORT + "/")
    r = requests.get(url = socket_url)
    return r.content


@items_api.route('/ViewAllItems', methods=['POST'])
@expects_json(_view_items_schema)
def ViewAllItems():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ITEMS_PORT + "/ViewAllItems")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@items_api.route('/ViewFlaggedItems', methods=['GET'])
@expects_json(_view_items_schema)
def ViewFlaggedItems():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ITEMS_PORT + "/ViewFlaggedItems")
    r = requests.get(url = socket_url)
    return r.content


@items_api.route('/SearchItem', methods=['POST'])
@expects_json(_search_items)
def SearchItem():
    socket_url = ("http://" +ITEMS_SERVICE_HOST +
                     ITEMS_PORT + "/SearchItem")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@items_api.route('/AddUserToWatchlist', methods = ['POST'])
@expects_json(_watchlist)
def AddUserToWarchlist():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ITEMS_PORT + "/AddUserToWatchlist")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content



@items_api.route('/RemoveItem', methods = ['POST'])
@expects_json(_item)
def RemoveItem():
    if routes.view_bids().length == 0:
        return """There are already bids on 
                this item! It cannot be deleted"""
    
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ITEMS_PORT + "/RemoveItem")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@items_api.route('/ReportItem', methods = ['POST'])
@expects_json(_report)
def ReportItem():
    socket_url = ("http://" + ITEMS_SERVICE_HOST+
                     ITEMS_PORT + "/ReportItem")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@items_api.route("/GetItem", methods = ['POST'])
@expects_json(_item)
def GetItem():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ITEMS_PORT + "/GetItem")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@items_api.route("/ModifyItem", methods = ['POST'])
@expects_json(_unrequired_attributes)
def ModifyItem():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ITEMS_PORT + "/ModifyItem")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@items_api.route("/AddItem", methods = ['POST'])
@expects_json(_required_attributes)
def AddItem():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ITEMS_PORT + "/AddItem")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@items_api.route("/EditCategories", methods = ['POST'])
@expects_json(_category)
def EditCategories():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ITEMS_PORT + "/EditCategories")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@items_api.route("/ModifyAvailability", methods = ['POST'])
@expects_json(_item)
def ModifyAvailability():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ITEMS_PORT + "/ModifyAvailability")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content