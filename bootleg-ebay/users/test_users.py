import unittest
from unittest import TestCase

from users import User, Buyer, Seller, Admin

class TestUser(TestCase):

    
    @staticmethod
    def init_user():
        user_id = 'de940cec-8a2'
        username = 'favourable_mother_Oh'
        password = 'cousinno'
        user_info = {
            'email': 'for.he@lyft.com',
            'money': 309
        }
        
        user = User(user_id=user_id, username=username, password=password, user_info=user_info)

        return user

    def test_login(self):
        username = 'favourable_mother_Oh'
        password = 'cousinno'

        user = TestUser.init_user()

        # Check a successful log in
        logged_in = user.login(username, password)
        self.assertTrue(logged_in)
        user.logout()

        # Check unsuccessful log ins
        logged_in = user.login('incorrect_username', 'incorrect_password')
        self.assertFalse(logged_in)

        logged_in = user.login(username, 'incorrect_password')
        self.assertFalse(logged_in)

        logged_in = user.login('incorrect_username', password)
        self.assertFalse(logged_in)

    def test_modify_profile(self):
        username = 'favourable_mother_Oh'
        password = 'cousinno'
        new_password = 'new_password'
        new_username = 'new_username'
        new_money = 1000

        # check that we correctly modified the user information
        user = TestUser.init_user()
        user.login(username, password)
    
        user.modify_profile(password=new_password)
        self.assertEqual(user.password, new_password)

        user.modify_profile(username=new_username)
        self.assertEqual(user.username, new_username)

        user.modify_profile(user_info={'money': new_money})
        self.assertEqual(user.user_info['money'], new_money)

        user.logout()

        # check that a logged out user cannot modify profile
        with self.assertRaises(ValueError):
            user.modify_profile(user_info={'money': new_money})

    def test_suspend_account(self):
        user = TestUser.init_user()
        user.suspend_account()

        self.assertTrue(user.user_info['suspended'])

if __name__ == '__main__':
    unittest.main()