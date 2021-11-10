"""Test the payment mediator interface.
"""
import unittest
from unittest import TestCase
import requests
import random

from config import *
from utils import id_generator


def randint():
    return random.randint(0, 4294967295)

def randcard_number(): 
    return random.randint(1111111111111111, 9999999999999999)

class TestUser(TestCase):
    base_url = "{}/{}/".format(MEDIATOR_LINK, PAYMENTS_NAME)


    def test_card(self):
        card_number = randcard_number()
        user_id = randint()
        security_code = 123
        expiration_date = "2024-6-1"


        # create card successfully
        url = self.base_url + "card"
        card_info_params = {
            "user_id": user_id,
            "card_number": card_number,
            "security_code": security_code,
            "expiration_date": expiration_date
        }

        output = requests.post(url=url, json=card_info_params)
        self.assertTrue(output.ok)
        id_ = output.json()['payment_id']

        # check that creating account with an existing user id fails
        output = requests.post(url=url, json=card_info_params)
        self.assertFalse(output.ok)
        self.assertEqual(output.status_code, 400)

        # view successfully
        url = self.base_url + "card/{}".format(id_)
        output = requests.get(url=url, json=None)
        output_json = output.json()
        self.assertEqual(output_json["card_number"], card_number)
        self.assertEqual(output_json["expiration_date"], expiration_date)
        self.assertEqual(output_json["security_code"], security_code)
        self.assertTrue(output.ok)

        # get by user id
        url = self.base_url + "card_by_user/{}".format(user_id)
        output = requests.get(url=url, json=None)
        output_json = output.json()
        self.assertEqual(output_json["card_number"], card_number)
        self.assertEqual(output_json["expiration_date"], expiration_date)
        self.assertEqual(output_json["security_code"], security_code)
        self.assertTrue(output.ok)

        # delete successfully
        url = self.base_url + 'card/{}'.format(id_)
        output = requests.delete(url=url, json=None)
        self.assertTrue(output.ok)

    def test_transaction(self):

        user_id = 22
        payment_id = 213
        item_id = "sdsadsa"
        money = 10.5
        quantity = 2

        # create successfully
        url = self.base_url + "transaction"
        transaction_info = {
            "user_id": user_id,
            "payment_id": payment_id,
            "item_id": item_id,
            "money": money,
            "quantity": quantity
        }

        output = requests.post(url=url, json=transaction_info)
        self.assertTrue(output.ok)
        id_ = output.json()['transaction_id']


        # view successfully
        url = self.base_url + "transaction/{}".format(id_)
        output = requests.get(url=url, json=None)
        output_json = output.json()
        self.assertEqual(output_json["user_id"], user_id)
        self.assertEqual(output_json["payment_id"], payment_id)
        self.assertEqual(output_json["item_id"], item_id)
        self.assertEqual(output_json["money"], money)
        self.assertEqual(output_json["quantity"], quantity)
        self.assertTrue(output.ok)

        # delete successfully
        output = requests.delete(url=url, json=None)
        self.assertTrue(output.ok)




