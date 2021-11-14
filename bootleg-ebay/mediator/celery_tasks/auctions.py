import requests

import celery
from flask import Response

from config import *

@celery.shared_task(name='celery_tasks.add_together')
def add_together(x, y):
    return x + y

@celery.shared_task(name='celery_tasks.end_auction_actions')
def end_auction_actions(auction_id):
    """This should be called when an auction finishes
    """

    socket_url = AUCTIONS_URL + "/auction/{}".format(auction_id)
    output = requests.get(url=socket_url, json=None)
    output_json = output.json()

    # if we can't find the auction because it has been deleted
    if not output.ok:
        return

    socket_url = CARTS_URL + "/add_item_to_cart"

    data = {
        "item_id": output_json['item_id'], 
        'user_id': output_json['bids'][-1]['buyer_id'] 
    }
    r = requests.post(url=socket_url, json=data)

    if not r.ok:
        return Response(response=r.text, status=r.status_code)
