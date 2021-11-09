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
        'seller_id': {'type': 'integer'},
        'bids': {'type': 'array'}
    },
    'required': ['start_time', 'end_time', 'item_id', 'seller_id']
}

_auction = {
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
        'user_id': {'type': 'integer'}
    },
    'required': ['user_id']
}

_bid = {
    'type': 'object',
    'properties': {
        'user_id': {'type': 'integer'},
        'auction_id': {'type': 'string'},
        'price': {'type': 'number'}
    },
    'required': ['user_id', 'auction_id', 'price']
}



auctions_api = Blueprint('auctions', __name__)


@auctions_api.route("/auction", methods = ['POST'])
@expects_json(_create)
def create_auction():
    socket_url = (AUCTIONS_URL + "/auction")
    r = get_and_request(socket_url, 'post')
    
    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content


@auctions_api.route("/auction/<auction_id>", methods = ['GET'])
# @expects_json(_none_schema)
def get_auction(auction_id):
    socket_url = (AUCTIONS_URL + "/auction/{}".format(auction_id))
    r = get_and_request(socket_url, 'get')
    
    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content

@auctions_api.route("/current_auctions", methods = ['GET'])
# @expects_json(_none_schema)
def view_current_auctions():
    socket_url = (AUCTIONS_URL + "/current_auctions")

    r = get_and_request(socket_url, 'get')
    
    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content



@auctions_api.route("/auction/<auction_id>", methods = ['DELETE'])
# @expects_json(_none_schema)
def remove_auction(auction_id):
    socket_url = AUCTIONS_URL + "/auction/{}".format(auction_id)
    r = get_and_request(socket_url, 'delete')
    
    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content


@auctions_api.route("/bids/<user_id>", methods = ['GET'])
# @expects_json(_none_schema)
def user_bids(user_id):
    socket_url = (AUCTIONS_URL + "/bids/{}".format(user_id))
    r = get_and_request(socket_url, 'get')
    
    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content


@auctions_api.route("/bid", methods = ['POST'])
@expects_json(_bid)
def create_bid():
    socket_url = (AUCTIONS_URL + "/bid")
    r = get_and_request(socket_url, 'post')
    
    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content

@auctions_api.route("/<auction_id>/bids", methods = ['GET'])
# @expects_json(_auction)
def view_bids(auction_id):
    socket_url = AUCTIONS_URL + "/{}/bids".format(auction_id)
    r = get_and_request(socket_url, 'get')
    
    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content
