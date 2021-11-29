"""Test the carts mediator interface.
"""
import unittest
from unittest import TestCase
import requests

from config import *
from utils import id_generator, current_time
import json
from bson.objectid import ObjectId

class TestCart(TestCase):
    base_url = "{}/{}/".format(MEDIATOR_LINK, CARTS_NAME)

    def test_cart(self):

        # create cart successfully
        url = self.base_url + "cart"
        user = {"user_id" : 400}
        output = requests.post(url = url, json = user)
        self.assertTrue(output.ok)

        cart_id = output.json()["_id"]

        # add item, get cart, then remove it
        url = self.base_url + "addition"
        item = {'user_id': 1, 'item_id': "619538ad26e831839aaa22c1"}
        output = requests.post(url = url, json = item)
        self.assertTrue(output.ok)

        url = self.base_url + "cart/%s" % str(400)
        output = requests.get(url=url)
        self.assertTrue(output.ok)

        url = self.base_url + "removal"
        output = requests.post(url = url, json = item)
        self.assertTrue(output.ok)

        # add item then empty cart
        url = self.base_url + "addition"
        output = requests.post(url = url, json = item)
        self.assertTrue(output.ok)

        url = self.base_url + "empty"
        output = requests.post(url = url, json = {"user_id": 1})
        self.assertTrue(output.ok)

        # add item to cart successfully
        url = self.base_url + "addition"
        item = {'item_id': "619538ad26e831839aaa22c1",
                'user_id': 1}
        output = requests.post(url = url, json = item)
        self.assertTrue(output.ok)


        # checkout

        # I must create an auction for this item
        start_time = current_time() - 20000

        auction_info = {
            "start_time": int(start_time),
            "end_time": int(current_time() + 10000),
            "item_id": "619538ad26e831839aaa22c1",
            "seller_id": 7,
            'shipping': 10.0,
            'buy_now': True,
            'buy_now_price': 25.0,
            'starting_price': 5.0,
            'completed': False,
            "bids": []
        }

        url = MEDIATOR_LINK + "/auctions/auction"
        output = requests.post(url=url, json=auction_info)
        auction_id = output.json()['auction_id']
        self.assertTrue(output.ok)


        url = self.base_url + "checkout"
        output = requests.post(url=url, json={"user_id": 1})

        """
        # delete auction successfully
        url = MEDIATOR_LINK + "/auctions/auction/{}".format(auction_id)
        output = requests.delete(url=url, json=None)
        self.assertTrue(output.ok)
        """

        # SECOND CHECKOUT CASE... AUCTION CASE

         # add item to cart successfully
        url = self.base_url + "addition"
        item = {'item_id': "619538ad26e831839aaa22c1",
                'user_id': 1}
        output = requests.post(url = url, json = item)
        self.assertTrue(output.ok)
        # I must create an auction for this item
        # the user this time will buy the item.
        start_time = current_time() - 20000

        auction_info = {
            "start_time": int(start_time),
            "end_time": int(current_time()) - 1000,
            "item_id": "619538ad26e831839aaa22c1",
            "seller_id": 7,
            'shipping': 10.0,
            'buy_now': True,
            'buy_now_price': 45.0,
            'starting_price': 5.0,
            'completed': False,
            "bids": [{'buyer_id': 1, 'price': 10, "bid_time": int(current_time() - 2), "bid_id": str(ObjectId())}]
        }

        url = MEDIATOR_LINK + "/auctions/auction"
        output = requests.post(url=url, json=auction_info)
        auction_id = output.json()['auction_id']
        self.assertTrue(output.ok)

        url = self.base_url + "checkout"
        output = requests.post(url=url, json={"user_id": 1})

        # remove cart completely
        url = self.base_url + "remove_cart"
        output = requests.post(url = url, json = {"user_id": 400})
        self.assertTrue(output.ok)
        
        """
        # delete auction successfully
        url = MEDIATOR_LINK + "/auctions/auction/{}".format(auction_id)
        output = requests.delete(url=url, json=None)
        self.assertTrue(output.ok)
        """
        