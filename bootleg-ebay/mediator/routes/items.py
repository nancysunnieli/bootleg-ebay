import requests
import os
import requests
import json

from flask_expects_json import expects_json
from flask import Response, request

from utils import get_and_post
from . import routes
from config import *


# getting IP Address of items container
# The following functions call the items microservice


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





@routes.route('/Items/', methods=['GET'])
def ItemsServiceStatus():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ":8099" + "/")
    r = requests.get(url = socket_url)
    return r.content

@app.route('/Items/ViewAllItems', methods=['POST'])
@expects_json(_view_items_schema)
def ViewAllItems():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ":8099" + "/ViewAllItems")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@routes.route('/Items/ViewFlaggedItems', methods=['POST'])
@expects_json(_view_items_schema)
def ViewFlaggedItems():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ":8099" + "/ViewFlaggedItems")
    r = requests.get(url = socket_url)
    return r.content

@routes.route('/Items/SearchItem', methods=['POST'])
@expects_json(_search_items)
def SearchItem():
    socket_url = ("http://" +ITEMS_SERVICE_HOST +
                     ":8099" + "/SearchItem")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@routes.route('/Items/AddUserToWatchlist', methods = ['POST'])
@expects_json(_watchlist)
def AddUserToWatchlist():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ":8099" + "/AddUserToWatchlist")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@routes.route('/Items/RemoveItem', methods = ['POST'])
@expects_json(_item)
def RemoveItem():
    if routes.view_bids().length == 0:
        return """There are already bids on 
                this item! It cannot be deleted"""
    
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ":8099" + "/RemoveItem")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@routes.route('/Items/ReportItem', methods = ['POST'])
@expects_json(_report)
def ReportItem():
    socket_url = ("http://" + ITEMS_SERVICE_HOST+
                     ":8099" + "/ReportItem")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@routes.route("/Items/GetItem", methods = ['POST'])
@expects_json(_item)
def GetItem():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ":8099" + "/GetItem")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@routes.route("/Items/ModifyItem", methods = ['POST'])
@expects_json(_unrequired_attributes)
def ModifyItem():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ":8099" + "/ModifyItem")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@routes.route("/Items/AddItem", methods = ['POST'])
@expects_json(_required_attributes)
def AddItem():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ":8099" + "/AddItem")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@routes.route("/Items/EditCategories", methods = ['POST'])
@expects_json(_category)
def EditCategories():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ":8099" + "/EditCategories")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@routes.route("/Items/ModifyAvailability", methods = ['POST'])
@expects_json(_item)
def ModifyAvailability():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ":8099" + "/ModifyAvailability")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content