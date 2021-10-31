from abc import ABC, abstractmethod
import json
from typing import Any, Dict, Optional

class User(ABC):
    """Abstract class for the user

    Args:
        user_id: The unique id for the user
        username: Username of the user
        password: Password for the user
        user_info: User information regarding the user
    """
    def __init__(self, user_id: str, username: str, password: str, user_info: Dict[str, Any]) -> None:
        self._user_id = user_id
        self._username = username
        self._password = password
        self._user_info = {'email': None, 'money': 0, 'suspended': False}

        for k in user_info.keys():
            if k not in self._user_info:
                raise ValueError('You cannot have key: {} for `user_info`'.format(k))

        self._user_info.update(user_info)

        # self._logged_in = False

        if user_info['email'] is None:
            raise ValueError('You must provide an email!')


    @property
    def user_id(self):
        return self._user_id

    @property
    def password(self):
        return self._password

    @property
    def username(self):
        return self._username
    
    @property
    def user_info(self):
        return self._user_info

    
    @classmethod
    def from_dict(cls, dict_: Dict[str, Any]):
        """Initialize the class from a dictionary.

        This method is particularly useful for interacting with databases

        Returns
        """

        user_info = {
            'email': dict_['email'],
            'money': dict_['money'],
            'suspended': dict_['suspended']
        }

        new_instance = cls(
            user_id=dict_['id'],
            username=dict_['username'],
            password=dict_['password'],
            user_info=user_info
            )

        return new_instance

    def to_dict(self):
        """Convert the important methods to dictionary
        """

        user_info = {
            'id': self.user_id,
            'username': self.username,
            'password': self.password,
            'email': self.user_info['email'],
            'money': self.user_info['money'],
            'suspended': self.user_info['suspended']
        }

        return user_info

    def to_json(self):
        user_info = self.to_dict()
        return json.dumps(user_info)



    def _assert_not_suspended(self, operation):
        if self._user_info['suspended']:
            raise ValueError('You cannot perform {} because you are suspended'.format(operation))

    def _assert_logged_in(self, operation):
        if self._logged_in is False:
            raise ValueError('You must be logged in first before you do this operation: {}'.format(operation))

    def login(self, username: str, password) -> bool:
        """Login to the user account with the username and password

        Args:
            username: Username to login with
            password: Password to login with

        Returns:
            True if currently logged in, False otherwise

        """

        if username == self._username and password == self._password:
            self._logged_in = True
            return True
        else:
            return False

    def logout(self) -> None:
        """Logout from the user account
        """
        self._logged_in = False

    def suspend_account(self) -> None:
        """Suspend own account
        """

        self._user_info['suspended'] = True

    def modify_profile(
        self, 
        username: Optional[str] = None, 
        password: Optional[str] = None, 
        user_info: Optional[Dict[str, Any]] = None) -> None:
        """Update the profile information

        Args:
            username: Updated username
            password: Updated password
            user_info: Updated user information
        """

        operation = 'modify_profile'
        self._assert_not_suspended(operation=operation)
        # self._assert_logged_in(operation=operation)
    

        if username is not None:
            self._username = username

        if password is not None:
            self._password = password

        if user_info is not None:
            for k in user_info.keys():
                if k not in self._user_info:
                    raise ValueError('You cannot have key: {} for `user_info`'.format(k))

            self._user_info.update(user_info)



class Buyer(User):
    """The buyer
    """
    def __init__(self, **kwargs):
        super(Buyer, self).__init__(**kwargs)
        # self._watch_list = []
    
    # def place_item_on_watchlist(self, item) -> None:
    #     """Place an item to the buyer's watch list
    #     """
    #     self._watch_list.append(item)


class Seller(User):
    """The seller
    """
    def __init__(self, **kwargs):
        super(Seller, self).__init__(**kwargs)

class Admin(User):
    """The administrator
    """
    def __init__(self, **kwargs):
        super(Admin, self).__init__(**kwargs)
