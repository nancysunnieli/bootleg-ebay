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
        url = self.base_url + "creation"
        user = {"user_id" : "test"}
        output = requests.post(url = url, json = user)
        self.assertTrue(output.ok)

        cart_id = output.json()["_id"]

        # add item it cart successfully
        url = self.base_url + "addition"
        item = {'item_id': "618c54028f3def6e8f10add5",
                'user_id': "herself_and_"}
        output = requests.post(url = url, json = item)
        self.assertTrue(output.ok)

        # get cart
        url = self.base_url + "cart"
        output = requests.post(url=url, json=user)
        self.assertTrue(output.ok)


        # checkout
        url = self.base_url + "checkout"
        output = requests.post(url=url, json=user)

        # add item then remove it
        url = self.base_url + "addition"
        item = {'user_id': 'test', 'item_id': "618c54028f3def6e8f10add5"}
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