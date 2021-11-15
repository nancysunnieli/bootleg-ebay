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
    
    r_json = r.json()
    # result = current_app.celery.send_task('celery_tasks.add_together',args=[121232,61232])

    # countdown = r_json['end_time'] - r_json['start_time']
    result = current_app.celery.send_task(
        'celery_tasks.end_auction_actions',args=[r_json['auction_id'],],
        eta=datetime.datetime.fromtimestamp(r_json['end_time']))

    # add_result = result.get()
    # print('Processing is {}'.format( add_result ))
    # print('XXXXXXX')

    if not r.ok:
        return Response(response=r.text, status=r.status_code)

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

    return r.content


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


    socket_url = (AUCTIONS_URL + "/auction/{}".format(auction_id))
    auction_info = get_and_request(socket_url, 'get').content
    auction_info = json.loads(auction_info)

    buyers = []
    for bid in auction_info["bids"]:
        buyers.append(bid["buyer_id"])
    seller_id = auction_info["seller_id"]

    # now I must get the contact information of the buyers
    # and seller
    socket_url = (USERS_URL + "/user/{}".format(seller_id))
    seller_info = json.loads(get_and_request(socket_url, 'get').content)
    seller_email = seller_info["email"]

    buyer_emails = []
    for buyer in buyers:
        socket_url = (USERS_URL + "/user/{}".format(buyer))
        buyer_info = json.loads(get_and_request(socket_url, 'get').content)
        buyer_emails.append(buyer_info["email"])

    # next I need to get the item_id
    item_id = auction_info["item_id"]

    # send email to seller
    socket_url = ("http://" + NOTIFS_SERVICE_HOST +
                    NOTIFS_PORT + "/seller_bid")
    data = json.dumps({"recipient": seller_email, "item_id": item_id})
    result = requests.post(url = socket_url, json = data)

    # send emails to buyers
    socket_url = ("http://" + NOTIFS_SERVICE_HOST +
                    NOTIFS_PORT + "/buyer_bid")
    for buyer_email in buyer_emails:
        data = json.dumps({"recipient": buyer_email, "item_id": item_id})
        requests.post(url = socket_url, json = data)

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
