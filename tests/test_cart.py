"""Test the carts mediator interface.
"""
import unittest
from unittest import TestCase
import requests

from config import *
from utils import id_generator, current_time
import json

class TestAuction(TestCase):
    base_url = "{}/{}/".format(MEDIATOR_LINK, CARTS_NAME)

    def test_cart(self):
        
        # create cart successfully
        url = self.base_url + "cart"
        user = {"user_id" : 40}
        output = requests.post(url = url, json = user)
        self.assertTrue(output.ok)

        cart_id = output.json()["_id"]

        # add item it cart successfully
        url = self.base_url + "addition"
        item = {'item_id': "618ecbd2864f5897415ff300",
                'user_id': 40}
        output = requests.post(url = url, json = item)
        self.assertTrue(output.ok)

        # get cart
        url = self.base_url + "cart/%s" % str(40)
        output = requests.get(url=url)
        self.assertTrue(output.ok)


        # checkout
        url = self.base_url + "checkout"
        output = requests.post(url=url, json=user)

        # add item then remove it
        url = self.base_url + "addition"
        item = {'user_id': 40, 'item_id': "618ecbd2864f5897415ff300"}
        output = requests.post(url = url, json = item)
        self.assertTrue(output.ok)

        url = self.base_url + "removal"
        output = requests.post(url = url, json = item)
        self.assertTrue(output.ok)

        # add item then empty cart
        url = self.base_url + "addition"
        output = requests.post(url = url, json = item)
        self.assertTrue(output.ok)

        url = self.base_url + "empty"
        output = requests.post(url = url, json = user)
        self.assertTrue(output.ok)