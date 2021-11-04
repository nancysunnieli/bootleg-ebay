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



@routes.route('/Items/', methods=['GET'])
def ItemsServiceStatus():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ":8099" + "/")
    r = requests.get(url = socket_url)
    return r.content

@app.route('/Items/ViewAllItems', methods=['POST'])
def ViewAllItems():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ":8099" + "/ViewAllItems")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@routes.route('/Items/ViewFlaggedItems', methods=['GET'])
def ViewFlaggedItems():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ":8099" + "/ViewFlaggedItems")
    r = requests.get(url = socket_url)
    return r.content

@routes.route('/Items/SearchItem', methods=['POST'])
def SearchItem():
    socket_url = ("http://" +ITEMS_SERVICE_HOST +
                     ":8099" + "/SearchItem")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@routes.route('/Items/AddUserToWatchlist', methods = ['POST'])
def AddUserToWarchlist():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ":8099" + "/AddUserToWatchlist")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@routes.route('/Items/RemoveItem', methods = ['POST'])
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
def ReportItem():
    socket_url = ("http://" + ITEMS_SERVICE_HOST+
                     ":8099" + "/ReportItem")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@routes.route("/Items/GetItem", methods = ['POST'])
def GetItem():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                     ":8099" + "/GetItem")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@routes.route("/Items/ModifyItem", methods = ['POST'])
def ModifyItem():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ":8099" + "/ModifyItem")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content


@routes.route("/Items/AddItem", methods = ['POST'])
def AddItem():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ":8099" + "/AddItem")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@routes.route("/Items/EditCategories", methods = ['POST'])
def EditCategories():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ":8099" + "/EditCategories")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@routes.route("/Items/ModifyAvailability", methods = ['POST'])
def ModifyAvailability():
    socket_url = ("http://" + ITEMS_SERVICE_HOST +
                    ":8099" + "/ModifyAvailability")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content