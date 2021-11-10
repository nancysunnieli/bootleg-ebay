"""Test the user mediator interface.
"""
import unittest
from unittest import TestCase
import requests
import random

from config import *
from utils import id_generator

class TestUser(TestCase):
    base_url = "{}/{}/".format(MEDIATOR_LINK, USERS_NAME)

    # comment / uncomment this decorator to skip test
    # @unittest.skip("Skipped because it runs correctly")
    def test_account(self):

        user_name = id_generator()
        password = "123"

        # create account successfully
        url = self.base_url + "user"
        user_info_params = {
            "username": user_name,
            "email": "jinli7255@gmail.com",
            "password": password,
            "is_admin": False,
            "suspended": False
        }

        output = requests.post(url=url, json=user_info_params)
        self.assertTrue(output.ok)
        id_ = output.json()['user_id']

        # check that creating account with an existing username fails
        output = requests.post(url=url, json=user_info_params)
        self.assertFalse(output.ok)
        self.assertEqual(output.status_code, 400)
        


        # try to login with wrong password
        url = self.base_url + "login"
        params = {
            "username": user_name,
            "password": "WRONG_PASSWORD"
        }

        output = requests.post(url=url, json=params)

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

        # logout
        url = self.base_url + "logout"
        output2 = requests.get(url=url, json=None)
        self.assertTrue(output2.ok)

        # view user 
        url = self.base_url + "user/{}".format(id_)
        output = requests.get(url=url, json=None)
        output_json = output.json()
        self.assertEqual(output_json['username'], user_name)
        self.assertEqual(output_json['password'], password)
        self.assertTrue(output.ok)

        # suspend the account
        url = self.base_url + "suspend"
        output = requests.put(url=url, json={'user_id': id_})
        output_json = output.json()
        self.assertEqual(output_json["suspended"], True)
        self.assertTrue(output.ok)

        # unsuspend the account
        url = self.base_url + "unsuspend"
        output = requests.put(url=url, json={'user_id': id_})
        output_json = output.json()
        self.assertEqual(output_json["suspended"], False)
        self.assertTrue(output.ok)

        # delete account
        # make sure to delete anything you create for testing
        url = self.base_url + 'user/{}'.format(id_)
        output = requests.delete(url=url, json={})

        self.assertTrue(output.ok)
        
    # @unittest.skip("Skipped because it runs correctly")
    def test_modify(self):

        user_name = id_generator()
        password = "123"

        # create account successfully
        url = self.base_url + "user"
        user_info_params = {
            "username": user_name,
            "email": "jinli7255@gmail.com",
            "password": password,
            "is_admin": False,
            "suspended": False
        }

        output = requests.post(url=url, json=user_info_params)
        self.assertTrue(output.ok)
        id_ = output.json()['user_id']


        new_user_name = id_generator()
        new_password = "new_password"
        new_email = "email"

        # modify account
        url = self.base_url + "user/{}".format(id_)
        output = requests.put(
            url=url, 
            json={
                'username': new_user_name,
                "password": new_password,
                'email': new_email
                }
        )

        output_json = output.json()
        
        self.assertEqual(output_json["username"], new_user_name)
        self.assertEqual(output_json["password"], new_password)
        self.assertEqual(output_json["email"], new_email)
        self.assertTrue(output.ok)

        # check that we can't change admin priviledges
        output = requests.put(
            url=url, 
            json={
                'is_admin': True
                }
        )
        self.assertFalse(output.ok)
        self.assertEqual(output.status_code, 400)

        # check that we can update ratings
        url = self.base_url + "user/rating/{}".format(id_)

        num_ratings = 5
        ratings = []
        for _ in range(num_ratings):
            rating = random.randint(1, 5)
            ratings.append(rating)
            output = requests.put(
                url=url, 
                json={
                    'rating': rating
                    }
            )
            self.assertTrue(output.ok)

        output_json = output.json()
        self.assertEqual(output_json['number_of_ratings'], num_ratings)
        self.assertEqual(output_json['total_rating'], sum(ratings))


        # check that we can't give a rating less than 1 or greater than 5
        for rating in [-1, 0, 6, 7]:
            output = requests.put(
                url=url, 
                json={
                    'rating': rating
                    }
            )
            self.assertFalse(output.ok)
            self.assertEqual(output.status_code, 400)


        # delete the account
        url = self.base_url + 'user/{}'.format(id_)
        output = requests.delete(url=url, json={})

        self.assertTrue(output.ok)


if __name__ == '__main__':
    unittest.main()

