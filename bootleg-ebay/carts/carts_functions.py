import csv
import json
import os
import re
import socket
import uuid

from pymongo import MongoClient
import Cart

class APIError(Exception):
    """All custom API Exceptions"""
    pass 

class BadInputError(APIError):
    """Custom bad input error class."""
    code = 400
    description = "Bad input Error"

class CartsDBManager:
    @classmethod
    def _init_carts_collection(cls):
        hostname = os.getenv('CARTSDBHOST', "localhost")
        client = MongoClient("mongodb://root:bootleg@" + hostname + ":27017")

        db = client["carts"]
        carts_collection = db["carts"]
        return carts_collection

    @classmethod
    def create_cart(cls, user_id):
        """
        This creates an empty cart for the user.
        This function is executed whenever a new user
        is created.
        """
        carts_collection = cls._init_carts_collection()
        shopping_cart = {}
        shopping_cart["user_id"] = user_id
        shopping_cart["items"] = []
        result = carts_collection.insert_one(shopping_cart)

        if len(list(carts_collection.find({ "_id": shopping_cart["_id"]}))) == 1:
                cart = list(carts_collection.find({ "_id": shopping_cart["_id"]}))[0]
                cart["_id"] = str(cart["_id"])
                return cart
        else:
             raise BadInputError("Cart was not successfully Created. Please Try Again.")

    @classmethod
    def add_item_to_cart(cls, user_id, item_id):
        """
        This adds an item to the user's cart
        """
        carts_collection = cls._init_carts_collection()

        query = { "user_id": user_id }
        modification = { "$addToSet": {"items" : item_id }}
        result = carts_collection.update_one(query, modification)

        if len(list(carts_collection.find(query))) == 0:
            raise BadInputError("User Does Not Exist.")
        if result.modified_count > 0:
            return "Successfully added item to Shopping Cart."
        elif item_id in set(list(carts_collection.find(query))[0]["items"]):
            raise BadInputError("Item was already in Shopping Cart.")
        else:
            raise BadInputError("Addition Failed. Please try again.")

    @classmethod
    def delete_item_from_cart(cls, user_id, item_id):
        """
        This deletes the specified item from the user's cart
        """
        carts_collection = cls._init_carts_collection()

        query = {"user_id": user_id}
        modification = {"$pull" : {"items" : item_id}}
        result = carts_collection.update_one(query, modification)

        if len(list(carts_collection.find(query))) == 0:
            raise BadInputError("User Does Not Exist.")
        if result.modified_count > 0:
            return "Successfully removed item to Shopping Cart."
        elif item_id not in set(list(carts_collection.find(query))[0]["items"]):
            raise BadInputError("Item was orginally not in Shopping Cart.")
        else:
            raise BadInputError("Removal Failed. Please try again.")

    @classmethod
    def get_items_from_cart(cls, user_id):
        """
        This gets a list of all the items in a selected
        user's cart
        """
        carts_collection = cls._init_carts_collection()
        query = {"user_id": user_id}
        results = list(carts_collection.find(query))[0]["items"]
        return json.dumps(results)
    
    @classmethod
    def empty_cart(cls, user_id):
        """
        This allows the user to checkout
        their current cart
        """
        carts_collection = cls._init_carts_collection()
        query = { "user_id": user_id }
        modification = { "$set": {"items" : [] }}
        result = carts_collection.update_one(query, modification)
        return "Successfully Emptied Cart!"
    
    @classmethod
    def remove_cart(cls, user_id):
        carts_collection = cls._init_carts_collection()
        query = {"user_id": user_id}
        result = carts_collection.delete_many(query)
        return "Successfully Removed Cart"
    


def create_cart(user_id):
    """
    This creates an empty cart for the user.
    This function is executed whenever a new user
    is created.
    """
    shopping_cart = Cart.Cart(user_id, [])
    dictionary_object = shopping_cart.to_mongo()

    return CartsDBManager.create_cart(dictionary_object["user_id"])


def add_item_to_cart(user_id, item_id):
    """
    This adds an item to the user's cart
    """
    items = json.loads(CartsDBManager.get_items_from_cart(user_id))
    shopping_cart = Cart.Cart(user_id, items)
    r = shopping_cart.add_item(item_id)
    if r == "ITEM SUCCESSFULLY ADDED":
        dict_object = shopping_cart.to_mongo()

        for item in dict_object["items"]:
            if item not in items:
                return CartsDBManager.add_item_to_cart(user_id, item)
    # I call this either way because it will give me an error message if
    # it did not work
    return CartsDBManager.add_item_to_cart(user_id, item_id)

def delete_item_from_cart(user_id, item_id):
    """
    This deletes the specified item from the user's cart
    """
    items = json.loads(CartsDBManager.get_items_from_cart(user_id))
    shopping_cart = Cart.Cart(user_id, items)
    r = shopping_cart.remove_item(item_id)
    if r == "ITEM SUCCESSFULLY REMOVED.":
        dict_object = shopping_cart.to_mongo()
        for i in range(0, len(items)):
            if items[i] not in dict_object["items"]:
                return CartsDBManager.delete_item_from_cart(int(user_id), items[i])
    # I call this either way because it will give me an error message if
    # it did not work
    return CartsDBManager.delete_item_from_cart(int(user_id), item_id)

def get_items(user_id):
    """
    This gets a list of all the items in a selected
    user's cart
    """
    return CartsDBManager.get_items_from_cart(user_id)

def empty_cart(user_id):
    """
    This allows the user to checkout
    their current cart
    """
    items = json.loads(CartsDBManager.get_items_from_cart(user_id))
    shopping_cart = Cart.Cart(user_id, items)

    shopping_cart.empty_cart()
    dict_object = shopping_cart.to_mongo()

    return CartsDBManager.empty_cart(dict_object["user_id"])

def remove_cart(user_id):
    """
    This removes the cart
    """
    return CartsDBManager.remove_cart(user_id)
    


if __name__ == "__main__":
    print("Create Cart Test: ")
    print(create_cart("3198005a-c85"))
    print("Add Item To Cart Test: ")
    print(add_item_to_cart("3198005a-c85", "48c00e9a-f5e"))
    print(add_item_to_cart("3198005a-c85", "c7ed9ede-00e"))
    print("Delete Item From Cart Test: ")
    print(delete_item_from_cart("3198005a-c85", "48c00e9a-f5e"))
    print("Get Items Test: ")
    print(get_items("3198005a-c85"))
    print(empty_cart("3198005a-c85"))





