"""Test the auction mediator interface.
"""
import unittest
from unittest import TestCase
import requests

from config import *
from utils import id_generator, current_time

class TestAuction(TestCase):
    base_url = "{}/{}/".format(MEDIATOR_LINK, AUCTIONS_NAME)

    def test_auction(self):
        

        # create auction successfully
        url = self.base_url + "auction"
        time = current_time()
        item_id = "sdsadsa"
        seller_id = 242312
        auction_info = {
            "start_time": time,
            "end_time": time + 1000000000,
            "item_id": item_id,
            "seller_id": seller_id
        }

        output = requests.post(url=url, json=auction_info)
        # import pdb; pdb.set_trace()
        self.assertTrue(output.ok)
        id_ = output.json()['auction_id']


        # view current auctions
        url = self.base_url + "current_auctions"
        output = requests.get(url=url, json={})
        self.assertTrue(output.ok)


        # create sucessful bids
        buyer_id1 =  12321
        buyer_id2 = 21454

        url = self.base_url + "bid"

        initial_price = 10.0
        price = initial_price
        for i in range(3):
            bid_info = {
                "price": price,
                "auction_id": id_,
                "user_id": buyer_id1
            }
            price += 0.3
            output = requests.post(url=url, json=bid_info)
            self.assertTrue(output.ok)

        for i in range(4):
            bid_info = {
                "price": price,
                "auction_id": id_,
                "user_id": buyer_id2
            }
            price += 0.3
            output = requests.post(url=url, json=bid_info)
            self.assertTrue(output.ok)

        # make unsuccessful bid (bid is lower than max bid)
        bid_info = {
            "price": initial_price,
            "auction_id": id_,
            "user_id": buyer_id2
        }
        output = requests.post(url=url, json=bid_info)
        self.assertFalse(output.ok)
        self.assertEqual(output.status_code, 400)

        # delete auction successfully
        url = self.base_url + "auction/{}".format(id_)
        output = requests.delete(url=url, json={})
        self.assertTrue(output.ok)
