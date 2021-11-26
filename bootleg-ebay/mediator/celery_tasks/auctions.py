import requests
import json

import celery
from flask import Response

from config import *

# NOTE: don't use request.get_json() for celery tasks. This will create bugs
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

@celery.shared_task(name='celery_tasks.bid_alert')
def bid_alert(auction_id):
    """Call this asynchronous task whenever some one places a bid
    """

    socket_url = AUCTIONS_URL + "/auction/{}".format(auction_id)
    r = requests.get(url=socket_url, json=None)
    if not r.ok:
        return Response(response=r.text, status=r.status_code)
    auction_info = r.json()

    # send email to seller
    socket_url = USERS_URL + "/user/{}".format(auction_info["seller_id"])
    r = requests.get(url=socket_url, json=None)
    if not r.ok:
        return Response(response=r.text, status=r.status_code)
    seller_email = r.json()["email"]

    socket_url = NOTIFS_URL + "/seller_bid"
    data = {"recipient": seller_email, "auction_id": auction_id}
    r = requests.post(url=socket_url, json=data)
    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    # send email to buyers, except for the latest buyer
    buyer_ids = []
    for bid in auction_info["bids"]:
        buyer_ids.append(bid["buyer_id"])
    buyer_ids = list(set(buyer_ids))
    latest_buyer_id = max(auction_info['bids'], key=lambda x: x['price'])['buyer_id']
    buyer_ids.remove(latest_buyer_id)

    for b_id in buyer_ids:
        socket_url = USERS_URL + "/user/{}".format(b_id)
        r = requests.get(url=socket_url, json=None)
        if not r.ok:
            return Response(response=r.text, status=r.status_code)

        buyer_info = r.json()

        socket_url = NOTIFS_URL + "/buyer_bid"
        data = {"recipient": buyer_info["email"], "auction_id": auction_id}
        requests.post(url = socket_url, json = data)


@celery.shared_task(name='celery_tasks.watch_list_alert')   
def watch_list_alert(auction_id):
    """Execute this when an auction goes live and we want to alert the people watching the items
    """
    # raise NotImplementedError
    socket_url = AUCTIONS_URL + "/auction/{}".format(auction_id)
    r = requests.get(url=socket_url, json=None)

    # if we can't find the auction because it has been deleted
    if not r.ok:
        return

    auction_info = r.json()

    url = ITEMS_URL + "/get_item"
    item = json.dumps({"item_id": auction_info['item_id']})
    r = requests.post(url=url, json=item)
    if not r.ok:
        return Response(response=r.text, status=r.status_code)

    # send email out to everyone on the item watch list
    user_ids = r.json()['watchlist']
    for user_id in user_ids:
        socket_url = USERS_URL + "/user/{}".format(user_id)
        r = requests.get(url=socket_url, json=None)
        if not r.ok:
            return Response(response=r.text, status=r.status_code)

        user_info = r.json()

        socket_url = NOTIFS_URL + "/watchlist"
        data = {"recipient": user_info["email"], "auction_id": auction_id}
        requests.post(url=socket_url, json=data)