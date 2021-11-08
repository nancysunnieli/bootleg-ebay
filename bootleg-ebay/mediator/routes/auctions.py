import os
import requests
import json

from flask_expects_json import expects_json
from flask import Response, request, Blueprint

from utils import get_and_request
from config import *

# getting IP Address of auctions container
# The following are functions for the auctions microservice


_create = {
    'type': 'object',
    'properties': {
        'start_time': {'type': 'number'},
        'end_time': {'type': 'number'},
        'item_id': {'type': 'string'},
        'seller_id': {'type': 'string'},
        'bids': {'type': 'array'}
    },
    'required': ['start_time', 'end_time', 'item_id', 'seller_id']
}

_item = {
    'type': 'object',
    'properties': {
        'auction_id' : {'type': 'string'}
    },
    'required': ['auction_id']
}
_none_schema = {
    'type': 'object',
    'properties': {
    },
    'required': []
}

_user = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'string'}
    },
    'required': ['user_id']
}

_bid = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'string'},
        'item_id': {'type': 'string'}
    },
    'required': ['user_id', 'item_id']
}



auctions_api = Blueprint('auctions', __name__)


@auctions_api.route("/auction", methods = ['POST'])
@expects_json(_create)
def create_auction():
    socket_url = ("http://" + AUCTIONS_SERVICE_HOST + AUCTIONS_PORT + "/auction")
    r = get_and_request(socket_url, 'post')
    
    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content


@auctions_api.route("/auction/<auction_id>", methods = ['GET'])
@expects_json(_none_schema)
def get_auction(auction_id):
    socket_url = ("http://" + AUCTIONS_SERVICE_HOST + AUCTIONS_PORT + "/auction/{}".format(auction_id))
    r = get_and_request(socket_url, 'get')
    
    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content

@auctions_api.route("/current_auctions", methods = ['GET'])
@expects_json(_none_schema)
def view_current_auctions():
    socket_url = ("http://" + AUCTIONS_SERVICE_HOST + AUCTIONS_PORT + "/current_auctions")

    r = get_and_request(socket_url, 'get')
    
    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content



@auctions_api.route("/auction/<auction_id>", methods = ['DELETE'])
@expects_json(_none_schema)
def remove_auction(auction_id):
    socket_url = "http://" + AUCTIONS_SERVICE_HOST + AUCTIONS_PORT + "/auction/{}".format(auction_id)
    r = get_and_request(socket_url, 'delete')
    
    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content


@auctions_api.route("/bids_by_user", methods = ['POST'])
@expects_json(_user)
def bids_by_user():
    socket_url = ("http://" + AUCTIONS_SERVICE_HOST + AUCTIONS_PORT + "/bids_by_user")
    return get_and_post(socket_url)


@auctions_api.route("/create_bid", methods = ['POST'])
@expects_json(_bid)
def create_bid():
    socket_url = ("http://" + AUCTIONS_SERVICE_HOST + AUCTIONS_PORT + "/create_bid")
    return get_and_post(socket_url)

@auctions_api.route("/view_bids", methods = ['POST'])
@expects_json(_item)
def view_bids():
    socket_url = ("http://" + AUCTIONS_SERVICE_HOST + AUCTIONS_PORT + "/view_bids")
    return get_and_post(socket_url)
