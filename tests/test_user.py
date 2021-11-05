"""Test the user mediator interface.
"""
import unittest
from unittest import TestCase
import requests

from config import *


class TestUser(TestCase):
    base_url = "{}/{}/".format(MEDIATOR_LINK, USERS_NAME)

    # comment / uncomment this decorator to skip test
    # @unittest.skip("Skipped because it runs correctly")
    def test_create_account(self):

        user_name = "jin903"
        password = "123"

        # create account successfully
        url = self.base_url + "create_account"
        params = {
            "username": user_name,
            "email": "jinli7255@gmail.com",
            "password": password,
            "is_admin": False,
            "suspended": False
        }

        output = requests.post(url=url, json=params)
        self.assertTrue(output.ok)

        # check that creating account with an existing username fails
        output = requests.post(url=url, json=params)
        self.assertFalse(output.ok)
        self.assertEqual(output.status_code, 400)
        


        # try to login with wrong password
        url = self.base_url + "login"
        params = {
            "username": user_name,
            "password": "WRONG_PASSWORD"
        }

        output = requests.post(url=url, json=params)
        # import pdb; pdb.set_trace()
        self.assertFalse(output.ok)
        self.assertEqual(output.status_code, 400)

        # login successfully
        url = self.base_url + "login"
        params = {
            "username": user_name,
            "password": password
        }

        output = requests.post(url=url, json=params)
        self.assertTrue(output.ok)


        # delete account
        # make sure to delete anything you create for testing
        url = self.base_url + 'delete_account'
        params = {
            "user_id": output.json()['id'],
        }
        output = requests.delete(url=url, json=params)

        self.assertTrue(output.ok)
        


if __name__ == '__main__':
    unittest.main()

