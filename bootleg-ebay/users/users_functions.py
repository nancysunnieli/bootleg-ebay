from re import L
import json
from typing import Dict, Any, Sequence, Optional, Union

from mysql.connector import connect, Error

from users import User, Admin, BadInputError





UserInfo = Dict[str, Any]
UserID = int

class UserDBManager:
    table_name = "users"
    table_cols = [
        "username", "password", 
        "email", 
        "suspended", "is_admin", 
        "total_rating", "number_of_ratings"]

    @classmethod
    def _create_connection(cls):
        connection = connect(
            host="users-db",
            port="3306",
            user="%s" % ("root"),
            password="%s" % ("bootleg"),
            database="users",
        )
        return connection

    @classmethod
    def insert_many(cls, data: Sequence):
        """Insert many rows into users database.

        Args: 
            data: List of rows to be inserted
        """
        cmd = "INSERT INTO {} ({}) VALUES ({})".format(
            cls.table_name, 
            ', '.join(cls.table_cols),
            ', '.join(['%s'] * len(cls.table_cols))
        )

        with cls._create_connection() as c:
            with c.cursor() as cursor:
                cursor.executemany(cmd, data)
            c.commit()
    
    @classmethod
    def update_by_id(cls, user_info: UserInfo) -> None:
        """Update the database by id
        """
        set_cmd = ["{} = %s".format(c) for c in cls.table_cols]
        set_cmd = ", ".join(set_cmd)
        cmd = "UPDATE {} SET {} WHERE user_id = %s".format(cls.table_name, set_cmd)
        val = [user_info[c] for c in cls.table_cols] + [user_info['user_id']]

        with cls._create_connection() as c:
            with c.cursor() as cursor:
                cursor.execute(cmd, val)
            c.commit()

    @classmethod
    def delete_by_id(cls, user_id: UserID) -> None:
        """Delete a row from the database by user id
        """
        cmd = "DELETE FROM {} WHERE user_id = %s".format(cls.table_name)
        val = (user_id, )

        with cls._create_connection() as c:
            with c.cursor() as cursor:
                cursor.execute(cmd, val)
            c.commit()

    @classmethod
    def _get_user_by_query(cls, cmd, val):
        with cls._create_connection() as c:
            with c.cursor(dictionary=True) as cursor:
                cursor.execute(cmd, val)

                user_info = cursor.fetchall()
                assert len(user_info) <= 1

                # I.e. we couldn't find the user
                if len(user_info) == 0:
                    return None 

                user_info = user_info[0]

        if user_info['is_admin']:
            user_class = Admin
        else:
            user_class = User

        user = user_class.from_dict(user_info)

        return user

    @classmethod
    def get_user(cls, user_id: UserID) -> Optional[User]:
        """Get the user from the database by user id

        Returns:
            user: Returns `None` if we couldn't find the user. Otherwise, return the user.
        """
        cmd = "SELECT * FROM {} WHERE user_id = %s".format(cls.table_name)
        val = (user_id,)

        user = cls._get_user_by_query(cmd, val)
        return user

    @classmethod
    def get_user_by_username(cls, username: str) -> Optional[User]:
        """Get the user from the database by username

        Returns:
            user: Returns `None` if we couldn't find the user. Otherwise, return the user.
        """

        cmd = "SELECT * FROM {} WHERE username = %s".format(cls.table_name)
        val = (username, )

        user = cls._get_user_by_query(cmd, val)
        return user

def _assert_not_none_user(user, user_id):
    if user is None:
        raise BadInputError('Cannot find user id {} in database'.format(user_id))

def view_user(user_id: UserID):
    user = UserDBManager.get_user(user_id)
    _assert_not_none_user(user, user_id)
    return user.to_json()
    
def view_user_by_username(username: str):
    user = UserDBManager.get_user_by_username(username)
    if user is None:
        raise BadInputError('Cannot find username {} in database'.format(username))
    return user.to_json()

def login(username, password) -> UserInfo:
    """Login to an account
    
    Returns:
        logged_in: Whether we logged in successfully or not
    """
    
    user = UserDBManager.get_user_by_username(username)

    if user is None:
        raise BadInputError('No existing username: {}'.format(username))
    if user.password != password:
        raise BadInputError('Wrong password!')

    if user.user_info["suspended"]:
        raise BadInputError("You are suspended and cannot login! ")

    return user.to_json()
    

def logout():
    """Log out from the account
    """
    return json.dumps({})

def create_account(user_info: UserInfo) -> UserInfo:
    """Create an user account.
    """
    # check if username already exists
    user = UserDBManager.get_user_by_username(user_info['username'])
    if user is not None:
        raise BadInputError('Username already exists!')

    row = []
    for c in UserDBManager.table_cols:
        if c not in user_info:
            if c == 'total_rating':
                default_val = 0
            elif c == 'number_of_ratings':
                default_val = 0
            else:
                raise ValueError('Not an optional column: {}'.format(c))

            row.append(default_val)
        else:
            row.append(user_info[c])

    rows = [row]
    UserDBManager.insert_many(rows)

    user = UserDBManager.get_user_by_username(user_info['username'])
    return user.to_json()

def suspend(user_id: UserID):
    """Suspend an user account.
    """
    user = UserDBManager.get_user(user_id)
    _assert_not_none_user(user, user_id)

    user.suspend()

    user_dict = user.to_dict()
    UserDBManager.update_by_id(user_dict)

    user = UserDBManager.get_user(user_id)
    return user.to_json()

def unsuspend(user_id: UserID):
    """Un-suspend an user account.
    """
    user = UserDBManager.get_user(user_id)
    _assert_not_none_user(user, user_id)

    user.unsuspend()

    user_dict = user.to_dict()
    UserDBManager.update_by_id(user_dict)

    user = UserDBManager.get_user(user_id)
    return user.to_json()

def modify_profile(new_user_info: UserInfo):
    """Modify the 

    Args:
        new_user_info: New user information to be updated
    """

    if 'username' in new_user_info:
        username = new_user_info['username']
        user = UserDBManager.get_user_by_username(username)

        if user is not None:
            raise BadInputError('Username already exists: {}'.format(username))

    
    user_id = new_user_info['user_id']
    del new_user_info['user_id']
    
    user = UserDBManager.get_user(user_id)
    _assert_not_none_user(user, user_id)

    user.modify_profile(
        user_info=new_user_info
    )

    user_dict = user.to_dict()

    UserDBManager.update_by_id(user_dict)

    user = UserDBManager.get_user(user_dict['user_id'])
    return user.to_json()

def update_rating(user_id: UserID, rating):
    user = UserDBManager.get_user(user_id)
    _assert_not_none_user(user, user_id)

    user.update_rating(rating)

    user_dict = user.to_dict()
    UserDBManager.update_by_id(user_dict)

    user = UserDBManager.get_user(user_id)
    return user.to_json()

def delete_account(user_id: UserID) -> None:
    UserDBManager.delete_by_id(user_id)

    return json.dumps({})


# delete_account(user_id=11)
# user = UserDBManager.get_user(10)

# import pdb; pdb.set_trace()