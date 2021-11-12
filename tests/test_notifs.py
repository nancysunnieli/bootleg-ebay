"""Test the notifications mediator interface.
"""
import unittest
from unittest import TestCase
import requests

from config import *
from utils import id_generator, current_time
import json

class TestNotifs(TestCase):
    base_url = "{}/{}/".format(MEDIATOR_LINK, NOTIFS_NAME)

    def test_notifs(self):
        
        # send watchlist notifcations
        url = self.base_url + "watchlist"
        schema = {
             "item_id": "618c54038f3def6e8f10add6",
             "recipient": "nancy_sunnie_li@yahoo.com"
        }
        output = requests.post(url=url, json=schema)
        self.assertTrue(output.ok)

        # send notif to seller bid
        url = self.base_url + "seller_bid"
        output = requests.post(url=url, json=schema)
        self.assertTrue(output.ok)

        # send notif to buyer bid
        url = self.base_url + "buyer_bid"
        output = requests.post(url=url, json=schema)
        self.assertTrue(output.ok)

        # send notif for time
        url = self.base_url + "time"
        schema = {
             "item_id": "618c54038f3def6e8f10add6",
             "recipient": "nancy_sunnie_li@yahoo.com",
             "time_left": "one day"
        }
        output = requests.post(url=url, json=schema)
        self.assertTrue(output.ok)

        # retrieve inbox
        url = self.base_url + "inbox"
        output = requests.get(url=url)
        self.assertTrue(output.ok)

