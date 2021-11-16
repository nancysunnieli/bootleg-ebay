"""Test the items mediator interface.
"""
import unittest
from unittest import TestCase
import requests

from config import *
from utils import id_generator, current_time
import json

class TestItem(TestCase):
    base_url = "{}/{}/".format(MEDIATOR_LINK, ITEMS_NAME)

    def test_item(self):
        
        # create item successfully
        url = self.base_url + "addition"
        item_info = {
            "name": "test",
            "description": "test",
            "category": ["Women's Clothing", "Shoes"],
            "photos": "618c53ec8f3def6e8f10adb9",
            "sellerID": 1,
            "price": 29.75,
            "quantity": 6,
            "shipping": 5}
        
        output = requests.post(url=url, json=item_info)
        self.assertTrue(output.ok)
        id_ = output.json()['_id']
        

        # view item 
        url = self.base_url + "item"
        item = {"item_id": id_}
        output = requests.post(url=url, json=item)
        self.assertTrue(output.ok)



        # view all items
        limit = {"limit": 10}
        url = self.base_url + "all_items"
        output = requests.post(url=url, json=limit)
        self.assertTrue(output.ok)

        # view all flagged items
        limit = {"limit": 10}
        url = self.base_url + "flagged_items"
        output = requests.post(url=url, json=limit)
        self.assertTrue(output.ok)

        # search
        search = {"keywords": ["and"]}
        url = self.base_url + "search"
        output = requests.post(url=url, json=search)
        self.assertTrue(output.ok)


        search = {"category": "Women's Clothing"}
        url = self.base_url + "search"
        output = requests.post(url=url, json=search)
        self.assertTrue(output.ok)

        # add to watchlist
        watchlist = {"item_id": id_, "user_id": 1}
        url = self.base_url + "watchlist"
        output = requests.post(url=url, json=watchlist)
        self.assertTrue(output.ok)

        # add item report
        report = {"item_id": id_, "reason": "counterfeit"}
        url = self.base_url + "report"
        output = requests.post(url=url, json=report)
        self.assertTrue(output.ok)

        # modify item
        modification = {"item_id": id_, "name": "test2"}
        url = self.base_url + "modification"
        output = requests.post(url=url, json=modification)
        self.assertTrue(output.ok)

        # change categories
        category = {"item_id": id_, "category": ["Shoes"]}
        url = self.base_url + "categories"
        output = requests.post(url=url, json=category)
        self.assertTrue(output.ok)

        # add lock on item
        url = self.base_url + "lock"
        item = {"item_id": id_}
        output = requests.post(url=url, json=item)
        self.assertTrue(output.ok)

        # delete item
        url = self.base_url + "removal"
        item = {"item_id": id_}
        output = requests.post(url=url, json=item)
        self.assertTrue(output.ok)

        # get all categories
        url = self.base_url + "all_categories"
        output = requests.get(url=url)
        self.assertTrue(output.ok)

        # add category
        url = self.base_url + "category_addition"
        category = {"category": "test"}
        output = requests.post(url=url, json=category)
        self.assertTrue(output.ok)

        # remove category
        url = self.base_url + "category_removal"
        category = {"category": "test"}
        output = requests.post(url=url, json=category)
        self.assertTrue(output.ok)