import csv
import json
import os
import re
import socket
import uuid

from pymongo import MongoClient

hostname = os.getenv('CARTSDBHOST', "localhost")
client = MongoClient("mongodb://root:bootleg@" + hostname + ":27020")

db = client["carts"]
carts_collection = db["carts"]

def create_cart(user_id, collection = carts_collection):
    """
    This creates an empty cart for the user.
    This function is executed whenever a new user
    is created.
    """
    shopping_cart = {}
    shopping_cart["user_id"] = user_id
    shopping_cart["items"] = []
    result = collection.insert_one(shopping_cart)

    if len(list(collection.find({ "_id": shopping_cart["_id"]}))) == 1:
            return "Cart Successfully Created!"
    else:
        return "Cart was not successfully Created. Please Try Again."


def add_item_to_cart(user_id, item_id, 
                    collection = carts_collection):
    """
    This adds an item to the user's cart
    """
    query = { "user_id": user_id }
    modification = { "$addToSet": {"items" : item_id }}
    result = collection.update_one(query, modification)

    if len(list(collection.find(query))) == 0:
        return "User Does Not Exist."
    if result.modified_count > 0:
        return "Successfully added item to Shopping Cart."
    elif item_id in set(list(collection.find(query))[0]["items"]):
        return "Item was already in Shopping Cart."
    else:
        return "Addition Failed. Please try again."

def delete_item_from_cart(user_id, item_id,
                            collection = carts_collection):
    """
    This deletes the specified item from the user's cart
    """
    query = {"user_id": user_id}
    modification = {"$pull" : {"items" : item_id}}
    result = collection.update_one(query, modification)

    if len(list(collection.find(query))) == 0:
            return "User Does Not Exist."
    if result.modified_count > 0:
        return "Successfully removed item to Shopping Cart."
    elif item_id not in set(list(collection.find(query))[0]["items"]):
        return "Item was orginally not in Shopping Cart."
    else:
        return "Removal Failed. Please try again."

def get_items(user_id, collection = carts_collection):
    """
    This gets a list of all the items in a selected
    user's cart
    """
    query = {"user_id": user_id}
    results = list(collection.find(query))[0]["items"]
    return json.dumps(results)

def checkout(user_id, colelction = carts_collection):
    """
    This allows the user to checkout their current cart
    """
    # FIGURE OUT HOW TO IMPLEMENT THIS
    pass

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





