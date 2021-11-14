"""Test the auction mediator interface.
"""
import unittest
from unittest import TestCase
import requests
import time

from config import *
from utils import id_generator, current_time

class TestAuction(TestCase):
    base_url = "{}/{}/".format(MEDIATOR_LINK, AUCTIONS_NAME)
    items_url = "{}/{}/".format(MEDIATOR_LINK, ITEMS_NAME)
    users_url = "{}/{}/".format(MEDIATOR_LINK, USERS_NAME)


    def _create_user(self):
        user_name = id_generator()
        password = "123"

        # create account successfully
        url = self.users_url + "user"
        user_info_params = {
            "username": user_name,
            "email": "jinli7255@gmail.com",
            "password": password,
            "is_admin": False,
            "suspended": False
        }

        output = requests.post(url=url, json=user_info_params)
        self.assertTrue(output.ok)
        user_id = output.json()['user_id']

        return user_id

    def _create_item(self):
        # create item successfully
        url = self.items_url + "addition"
        item_info = {
            "name": "test",
            "description": "test",
            "category": ["Women's Clothing", "Shoes"],
            "photos": "618c53ec8f3def6e8f10adb9",
            "sellerID": 10,
            "price": 29.75,
            "quantity": 6,
            "shipping": 5}
        
        output = requests.post(url=url, json=item_info)
        self.assertTrue(output.ok)
        item_id = output.json()['_id']

        return item_id

    def _delete_user(self, user_id):
        url = self.users_url + 'user/{}'.format(user_id)
        output = requests.delete(url=url, json={})
        self.assertTrue(output.ok)

    def _delete_users(self, user_ids):
        for user_id in user_ids:
            self._delete_user(user_id)

    def _delete_item(self, item_id):
        url = self.items_url + "removal"
        item = {"item_id": item_id}
        output = requests.post(url=url, json=item)
        self.assertTrue(output.ok)

    

    def test_auction(self):
        
        # create seller
        seller_id = self._create_user()

        # create buyers
        buyer_id1 = self._create_user()
        buyer_id2 = self._create_user()


        # create item id
        item_id = self._create_item()

        # duration of auction in terms of seconds
        auction_duration = 3

        # create auction successfully
        url = self.base_url + "auction"
        start_time = current_time()
        auction_info = {
            "start_time": start_time,
            "end_time": start_time + auction_duration,
            "item_id": item_id,
            "seller_id": seller_id,
            "bids": []
        }

        output = requests.post(url=url, json=auction_info)
        self.assertTrue(output.ok)
        id_ = output.json()['auction_id']

        # view auction
        url = self.base_url + "auction/{}".format(id_)
        output = requests.get(url=url, json=None)
        self.assertTrue(output.ok)

        # view auctions by item id
        url = self.base_url + "auctions_by_item/{}".format(item_id)
        output = requests.get(url=url, json=None)
        output_json = output.json()
        self.assertGreaterEqual(len(output_json), 1)
        self.assertTrue(output.ok)
        
        # view current auctions
        url = self.base_url + "current_auctions"
        output = requests.get(url=url, json=None)
        self.assertTrue(output.ok)


        # view auction metrics
        url = self.base_url + "auction_metrics"
        output = requests.post(url=url, json={'start': start_time, 'end': start_time + 1000000000})
        self.assertTrue(output.ok)
        
        # create sucessful bids
        buyer1_num_bids = 3
        buyer2_num_bids = 4
        
        url = self.base_url + "bid"

        initial_price = 10.0
        price = initial_price
        for _ in range(buyer1_num_bids):
            price += 0.3
            bid_info = {
                "price": price,
                "auction_id": id_,
                "buyer_id": buyer_id1
            }
            
            output = requests.post(url=url, json=bid_info)
            self.assertTrue(output.ok)

        for _ in range(buyer2_num_bids):
            price += 0.3
            bid_info = {
                "price": price,
                "auction_id": id_,
                "buyer_id": buyer_id2
            }
            
            output = requests.post(url=url, json=bid_info)
            self.assertTrue(output.ok)

        # view max bid price
        url = self.base_url + "auction/{}/max_bid".format(id_)
        output = requests.get(url=url, json=None)
        self.assertTrue(output.ok)
        self.assertEqual(output.json()['max_bid'], price)


        # make unsuccessful bid (bid is lower than max bid)
        url = self.base_url + "bid"
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

        time.sleep(auction_duration)


        # delete auction successfully
        url = self.base_url + "auction/{}".format(id_)
        output = requests.delete(url=url, json=None)
        self.assertTrue(output.ok)

        # delete created objects
        self._delete_users([buyer_id1, buyer_id2, seller_id])
        self._delete_item(item_id)

