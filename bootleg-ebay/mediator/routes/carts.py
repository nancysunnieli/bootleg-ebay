import os
import requests
import json

from flask_expects_json import expects_json
from flask import Response, request

from utils import get_and_post
from . import routes
from config import *

# getting IP Address of carts container
# The following are functions for the carts microservice

@routes.route("/Carts/CreateCart", methods = ['POST'])
def CreateCart():
    socket_url = ("http://" + CARTS_SERVICE_HOST +
                    ":3211" + "/CreateCart")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@routes.route("/Carts/AddItemToCart", methods = ['POST'])
def AddItemToCart():
    socket_url = ("http://" + CARTS_SERVICE_HOST +
                    ":3211" + "/AddItemToCart")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@routes.route("/Carts/DeleteItemFromCart", methods = ['POST'])
def DeleteItemFromCart():
    socket_url = ("http://" + CARTS_SERVICE_HOST +
                    ":3211" + "/DeleteItemFromCart")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@routes.route("/Carts/GetItemsFromCart", methods = ['POST'])
def GetItemsFromCart():
    socket_url = ("http://" + CARTS_SERVICE_HOST +
                    ":3211" + "/GetItemsFromCart")
    data_content = request.get_json()
    r = requests.post(url = socket_url, json = data_content)
    return r.content

@routes.route("/Carts/EmptyCart", methods = ['POST'])
def EmptyCart():
    socket_url = ("http://" + CARTS_SERVICE_HOST +
                    ":3211" + "/EmptyCart")
    data_content = request.get_json()
    r = requests.post(socket_url, json = data_content)
    return r.content

@routes.route("/Carts/Checkout", methods = ['POST'])
def Checkout():
    data_content = request.get_json()

    # gets all items in user's cart
    get_items_url = ("http://" + CARTS_SERVICE_HOST +
                    ":3211" + "/GetItemsFromCart")
    items = json.loads((requests.post(url = get_items_url, json = data_content)).content)


    # checks availability of all items
    items_availability_url = ("http://" + ITEMS_SERVICE_HOST +
                            ":8099" + "/GetItemsFromCart")
    available_items = []
    unavailable_items = []
    for item in items:
        availability = (requests.post(url = items_availability_url, data = {"item_id" : item})).content
        if availability == "Was unable to adjust availability. Item is no longer available.":
            unavailable_items.append(item)
        else:
            available_items.append(item)
    
    # GET CREDIT CARD INFO

    # CREATE PAYMENT INFO

    # DELETE ALL ITEMS FROM CART
    empty_cart_url = ("http://" + CARTS_SERVICE_HOST +
                    ":3211" + "/EmptyCart")
    r = requests.post(empty_cart_url, json = data_content)
    return r.content


