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
        self.assertTrue(output.ok)
        id_ = output.json()['auction_id']


        # view current auctions
        url = self.base_url + "current_auctions"
        output = requests.get(url=url, json=None)
        self.assertTrue(output.ok)


        # create sucessful bids
        buyer_id1 =  12321
        buyer_id2 = 21454
        buyer1_num_bids = 3
        buyer2_num_bids = 4

        url = self.base_url + "bid"

        initial_price = 10.0
        price = initial_price
        for _ in range(buyer1_num_bids):
            bid_info = {
                "price": price,
                "auction_id": id_,
                "user_id": buyer_id1
            }
            price += 0.3
            output = requests.post(url=url, json=bid_info)
            self.assertTrue(output.ok)

        for _ in range(buyer2_num_bids):
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

        # view all bids in that auction
        url = self.base_url + "/{}/bids".format(id_)
        output = requests.get(url=url, json=None)
        output_json = output.json()
        self.assertEqual(len(output_json), buyer1_num_bids + buyer2_num_bids)
        self.assertTrue(output.ok)

        # view bids by users
        for b_id in [buyer_id1, buyer_id2]:
            url = self.base_url + "bids/{}".format(b_id)
            output = requests.get(url=url, json=None)
            output_json = output.json()
            self.assertGreaterEqual(len(output_json), 1)
            self.assertTrue(output.ok)




        # delete auction successfully
        url = self.base_url + "auction/{}".format(id_)
        output = requests.delete(url=url, json=None)
        self.assertTrue(output.ok)
