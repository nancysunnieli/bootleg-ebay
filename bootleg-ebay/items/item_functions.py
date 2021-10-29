import pymongo
from pymongo import MongoClient
import csv
import uuid
import re
import json
import socket

hostname = socket.gethostbyname(socket.gethostname())
client = pymongo.MongoClient("mongodb://root:bootleg@" + hostname + ":27017")
db = client["items"]
items_collection = db["items"]
flagged_items_collection = db["flagged_items"]
photos_collection = db["photos"]


def ViewFlaggedItems(limit = None, collection = items_collection):
    """
    This returns all the flagged items
    """
    query = {"isFlagged": "True"}

    results = list(collection.find(query))
    if limit:
        return json.dumps(results[:limit])
    else:
        return json.dumps(results)

def EditCategories(item_id, updated_categories, collection = items_collection):
    query = { "_id" : item_id }
    new_categories = { "$set": { "category": updated_categories } }
    result = collection.update_one(query, new_categories)

    if result.modified_count > 0:
        return "Change was Successful!"
    else:
        return "Change was not Successful. Please Try Again."

def AddItem(name, description, category, photos, 
                sellerID, price,
                collection = items_collection):
    """
    This adds one item to our database
    """
    item = {"name": None, "description": None,
                "category": None, "photos": None, "sellerID": None,
                "price": None, "isFlagged": False, "watchlist": None}
    item["name"] = name
    item["description"] = description
    item["category"] = category
    item["photos"] = photos
    item["sellerID"] = sellerID
    item["price"] = price
    item["watchlist"] = []
    result = collection.insert_one(item)

    if len(list(collection.find({ "_id": item["_id"]}))) == 1:
        return "Item Successfully Inserted!"
    else:
        return "Item was not successfully inserted. Please Try Again."



def ModifyItem(id, name = None, description = None,
                category = None, photos = None, price = None,
                collection = items_collection):
    """
    With this function, I can modify the item
    that matches the given id.

    I can modify the name, description, category,
    photos, and price
    """
    query = { "_id" : id }
    modifications = []
    if name:
        new_name = { "$set": { "name": name } }
        modifications.append(new_name)
    if description:
        new_description = { "$set": { "description": description } }
        modifications.append(new_description)
    if category:
        new_categories = { "$set": { "category": category } }
        modifications.append(new_categories)
    if photos:
        new_photos = { "$set": { "photos": photos } }
        modifications.append(new_photos)
    if price:
        new_price = { "$set": { "price": price } }
        modifications.append(new_price)

    success = []
    failure = []
    for modification in modifications:
        result = collection.update_one(query, modification)
        if result.modified_count > 0:
            for key, value in modification["$set"].items():
                success.append(key)
        else:
            for key, value in modification["$set"].items():
                failure.append(key)

    string_to_return = ""
    if len(success) > 0:
        string_to_return += ("Successfully changed %s fields" % ", ".join(success))
    if len(failure) > 0:
        if string_to_return != "":
            string_to_return += " "
        string_to_return += ("Failure to change %s fields." % ", ".join(failure))
    return string_to_return

def GetItem(id, collection = items_collection):
    """
    given an item id, this function returns back the item
    """
    query = {"_id": id}
    results = json.dumps(list(collection.find(query)))
    return results

def AddFlaggedItem(item_id, flag_reason, collection = flagged_items_collection):
    """
    This adds a new flag to the database
    """
    item = {"itemID": item_id, "FlaggedReason": flag_reason}
    inserted_item = collection.insert_one(item)

    if len(list(collection.find({"_id" : inserted_item.inserted_id }))) == 1:
        return "Flag Successfully Added!"
    else:
        return "Flag Failure. Please Try Again."


def ReportItem(id, flag_reason, item_collection = items_collection, 
                flagged_item_collection = flagged_items_collection):
    """
    This flags an item, and gives the flag reason
    """
    # updates item database
    query = {"_id": id}
    flag = {"$set" : {"isFlagged" : "True" }}
    update_result = item_collection.update_one(query, flag)

    
    # updates flagged items database
    result = AddFlaggedItem(id, flag_reason)
    if (result == "Flag Successfully Added!"):
        return "Item Reported Successfully!"
    else:
        return "Item Report Failed. Please Try Again."

def RemoveItem(id, item_collection = items_collection,
                flagged_item_collection = flagged_items_collection):
    """
    This removes an item (if eligible)
    """
    # ADD IF STATEMENT THAT DOES NOT ALLOW ITEM TO BE
    # REMOVED IF THERE ARE ALREADY BIDS ON IT....
    # NEEDS TO CALL THE AUCTIONS MICROSERVICE
    if (False): # call to microservice
        return """There are already bids on 
                this item! It cannot be deleted"""

    find_item = {"_id": id}
    item_collection.delete_one(find_item)

    find_flags = {"itemID": id}
    flagged_item_collection.delete_many(find_flags)

    if (len(list(item_collection.find(find_item))) == 0
        and len(list(flagged_item_collection.find(find_flags))) == 0):
        return "Item Successfully Deleted."
    else:
        return "Item Was Not Deleted! Please Try Again."

def AddUserToWatchlist(id, user_id, collection = items_collection):
    """
    This adds a user to the watchlist
    """
    query = { "_id": id }
    modification = { "$addToSet": {"watchlist" : user_id }}
    result = collection.update_one(query, modification)

    if len(list(collection.find(query))) == 0:
        return "Item was not in the database."
    if result.modified_count > 0:
        return "Successfully added user to Watchlist."
    elif user_id in set(list(collection.find(query))[0]["watchlist"]):
        return "User was already in Watchlist."
    else:
        return "Addition Failed. Please try again."


def searchItem(keywords, collection = items_collection):
    """
    This searches the items in the database
    
    input:
    keywords (array of strings)
    """
    query = { "$or": []}
    for word in keywords:
        query["$or"].append({ "name" : {'$regex': word}})
        query["$or"].append({ "description" : {'$regex': word}})
    
    results = json.dumps(list(collection.find(query)))
    return results

# executing tests for my functions
if __name__ == '__main__':

    print("Search Item Test: ")
    print(searchItem(["lemon"]))
    
    print("Add User To Watchlist Test: ")
    print(AddUserToWatchlist("48c00e9a-f5e", "d35d484e-d66"))

    print("Remove Item From Items List Test: ")
    print(RemoveItem("48c00e9a-f5e"))

    print("Report Item Test/ Add Flagged Item Test: ")
    print(ReportItem("c7ed9ede-00e", "counterfeit"))

    print("Get Item Test: ")
    print(GetItem("c7ed9ede-00e"))

    print("Modify Item Test: ")
    print(ModifyItem("c7ed9ede-00e", "lemon bars"))

    print("Add Items: ")
    print(AddItem("potato test",
            "re you do by for and not almost of  I to  an dark but not ran",
            ["Jewelry", "Watches"], "0aa271bf-1b4", "492674a4-bbe",
            23.82))

    print("Edit Categories Test: ")
    print(EditCategories("48c00e9a-f5e", ["potato"]))

    print("View Flagged Items Test: ")
    print(ViewFlaggedItems())