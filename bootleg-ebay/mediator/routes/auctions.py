import os
import requests
import json
import datetime

from flask_expects_json import expects_json
from flask import Response, request, Blueprint, current_app

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
        'bids': {'type': 'array'},
        'shipping': {'type': 'number'},

        'buy_now': {'type': 'boolean'},
        'buy_now_price': {'type': 'number'},
        'starting_price': {'type': 'number'},
    },
    'required': [
        'start_time', 'end_time', 'item_id', 
        'seller_id', 
        'shipping', 
        'buy_now', 'buy_now_price', 'starting_price']
}

_modify = {
    'type': 'object',
    'properties': {
        'shipping': {'type': 'number'},
        'buy_now': {'type': 'boolean'},
        'buy_now_price': {'type': 'number'},
    },
    'required': []
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

_bid = {
    'type': 'object',
    'properties': {
        'buyer_id': {'type': 'integer'},
        'auction_id': {'type': 'string'},
        'price': {'type': 'number'}
    },
    'required': ['buyer_id', 'auction_id', 'price']
}

_time = {
    'type': 'object',
    'properties': {
        'start': {'type': 'number'},
        'end': {'type': 'number'}
    },
    'required': ['start', 'end']
}



auctions_api = Blueprint('auctions', __name__)


@auctions_api.route("/auction", methods = ['POST'])
@expects_json(_create)
def create_auction():
    socket_url = (AUCTIONS_URL + "/auction")
    r = get_and_request(socket_url, 'post')
    
    if not r.ok:
        return Response(response=r.text, status=r.status_code)
        
    r_json = r.json()

    start_time = datetime.datetime.fromtimestamp(r_json['start_time'])
    end_time = datetime.datetime.fromtimestamp(r_json['end_time'])

    result = current_app.celery.send_task(
        'celery_tasks.end_auction_actions',args=[r_json['auction_id'],],
        eta=end_time)

    result = current_app.celery.send_task(
        'celery_tasks.watch_list_alert',args=[r_json['auction_id'],],
        eta=start_time)


    # alert buyers and sellers before auction ends
    # TODO(jin): remove one second from this. One second is just for testing purposes
    times = [
        datetime.timedelta(days=1), 
        datetime.timedelta(hours=1), 
        datetime.timedelta(minutes=1),
        datetime.timedelta(seconds=1)]
    time_strs = ['One Day', 'One Hour', 'One Minute', 'One Second']

    for i, time_ in enumerate(times):
        # print("PRE_ALERT")
        eta = end_time - time_
        if eta < start_time:
            continue
        # print("ALERTING", time_strs[i])
        result = current_app.celery.send_task(
            'celery_tasks.alert_auction',args=[r_json['auction_id'], time_strs[i]],
            eta=eta)

    return r.content


@auctions_api.route("/auction/<auction_id>", methods = ['GET'])
def get_auction(auction_id):
    socket_url = (AUCTIONS_URL + "/auction/{}".format(auction_id))
    auction_r = get_and_request(socket_url, 'get')
    
    if not auction_r.ok:
        return Response(response=auction_r.text, status=auction_r.status_code)

    auction_info = auction_r.json()

    # get the username of the seller
    url = USERS_URL + "/user/{}".format(auction_info['seller_id'])
    r = requests.get(url=url, json=None)

    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    auction_info['seller_username'] = r.json()['username']

    # get username of each bidder
    for bid in auction_info['bids']:
        url = USERS_URL + "/user/{}".format(bid['buyer_id'])
        r = requests.get(url=url, json=None)

        if not r.ok:
            return Response(response=r.text, status=r.status_code)
        r_json = r.json()

        bid['buyer_username'] = r_json['username']

    return json.dumps(auction_info).encode(auction_r.encoding)
    # get the bidder username for each bid
    # return r.content

@auctions_api.route("/auction/<auction_id>", methods = ['PUT'])
@expects_json(_modify)
def modify_auction(auction_id):
    socket_url = (AUCTIONS_URL + "/auction/{}".format(auction_id))
    r = get_and_request(socket_url, 'put')
    
    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content

@auctions_api.route("/auction/<auction_id>/max_bid", methods = ['GET'])
def get_max_bid(auction_id):
    socket_url = (AUCTIONS_URL + "/auction/{}/max_bid".format(auction_id))
    r = get_and_request(socket_url, 'get')
    
    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content

@auctions_api.route("/auctions_by_item/<item_id>", methods = ['GET'])
def get_auctions_by_item_id(item_id):
    socket_url = (AUCTIONS_URL + "/auctions_by_item/{}".format(item_id))
    r = get_and_request(socket_url, 'get')
    
    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content


@auctions_api.route("/auction_metrics", methods = ['POST'])
@expects_json(_time)
def get_auction_metrics():
    socket_url = (AUCTIONS_URL + "/auction_metrics")

    r = get_and_request(socket_url, 'post')
    
    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content


@auctions_api.route("/finished_auctions", methods = ['GET'])
def view_finished_auctions():
    socket_url = (AUCTIONS_URL + "/finished_auctions")

    r = get_and_request(socket_url, 'get')
    
    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content

@auctions_api.route("/upcoming_auctions", methods = ['GET'])
def view_upcoming_auctions():
    socket_url = (AUCTIONS_URL + "/upcoming_auctions")

    r = get_and_request(socket_url, 'get')
    
    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content

@auctions_api.route("/current_auctions", methods = ['GET'])
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
    socket_url = AUCTIONS_URL + ("/bids/%s" % (user_id)) 
    r = get_and_request(socket_url, 'get')
    
    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    auctions_info = r.json()
    for a in auctions_info:
        socket_url = ITEMS_URL + ("/get_item") 
        data = json.dumps({"item_id": a['auction']["item_id"]})
        r = requests.post(url = socket_url, json=data)
        if not r.ok:
            return Response(response=r.text, status=r.status_code)
        a['item'] = r.json()

    return json.dumps(auctions_info)


@auctions_api.route("/bid", methods = ['POST'])
@expects_json(_bid)
def create_bid():
    
    socket_url = (AUCTIONS_URL + "/bid")
    r = get_and_request(socket_url, 'post')
    
    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    # notify the seller and buyers that there have been
    # new bids

    # first I need to get the seller and buyers in the auction
    data_content = request.get_json()
    auction_id = data_content["auction_id"]
    # username = data_content["buyer_id"]

    result = current_app.celery.send_task(
        'celery_tasks.bid_alert',args=[auction_id, ])

    # return new bid content
    return r.content

@auctions_api.route("/<auction_id>/bids", methods = ['GET'])
# @expects_json(_auction)
def view_bids(auction_id):
    socket_url = AUCTIONS_URL + "/{}/bids".format(auction_id)
    r = get_and_request(socket_url, 'get')
    
    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    return r.content
