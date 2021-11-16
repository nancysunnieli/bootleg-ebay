import requests
import json

import celery
from flask import Response

from config import *

# NOTE: don't use get_and_request for files under directory celery_tasks/
# NOTE: when modifying celery tasks, you have to restart docker for your code to see changes
@celery.shared_task(name='celery_tasks.add_together')
def add_together(x, y):
    return x + y

@celery.shared_task(name='celery_tasks.end_auction_actions')
def end_auction_actions(auction_id):
    """This should be called when an auction finishes
    """

    socket_url = AUCTIONS_URL + "/auction/{}".format(auction_id)
    output = requests.get(url=socket_url, json=None)

    # if we can't find the auction because it has been deleted
    if not output.ok:
        return

    output_json = output.json()

    socket_url = CARTS_URL + "/add_item_to_cart"

    user_id = max(output_json['bids'], key=lambda x: x['price'])['buyer_id']
    data = {
        "item_id": output_json['item_id'], 
        'user_id': user_id
    }
    r = requests.post(url=socket_url, json=data)

    if not r.ok:
        return Response(response=r.text, status=r.status_code)

@celery.shared_task(name='celery_tasks.alert_auction')
def alert_auction(auction_id, time_left):
    """This should be called when some time before an auction finishes
    """

    socket_url = AUCTIONS_URL + "/auction/{}".format(auction_id)
    output = requests.get(url=socket_url, json=None)

    # if we can't find the auction because it has been deleted
    if not output.ok:
        return

    auction_info = output.json()

    # get the buyer and seller ids
    ids = [auction_info["seller_id"]]
    for bid in auction_info["bids"]:
        ids.append(bid["buyer_id"])
    ids = list(set(ids))

    # send notifications to buyers and seller
    for id_ in ids:

        # get email
        socket_url = USERS_URL + "/user/{}".format(id_)
        # r = get_and_request(socket_url, 'get')
        r = requests.get(url=socket_url, json=None)

        if not r.ok:
            return Response(response=r.text, status=r.status_code)

        email = r.json()["email"]

        # send time left email
        socket_url = NOTIFS_URL + "/time"
        data = {
            "recipient": email, 
            "auction_id": auction_info['auction_id'],
            "time_left": time_left
        }
        r = requests.post(url=socket_url, json=data)

        if not r.ok:
            return Response(response=r.text, status=r.status_code)
