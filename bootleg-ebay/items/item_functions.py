import pymongo
from pymongo import MongoClient
import csv
from .items import Item

client = pymongo.MongoClient("mongodb://root:bootleg@localhost:27017")
db = client["items"]
items_collection = db["items"]
flagged_items_collection = db["flagged_items"]
photos_collection = db["photos"]

def create_items_database(data_file_path, collection = items_collection):
    """
    This creates the items database in mongo db with
    the fake data in the mock_data folder.

    Schema for items: id, name, description,
            category, photos, sellerID,
            price, isFlagged
    """

    file = open(data_file_path)
    csvreader = csv.reader(file)
    all_items = []
    for row in csvreader:
        item = {"_id": None, "name": None, "description": None,
                "category": None, "photos": None, "sellerID": None,
                "price": None, "isFlagged": None}
        item["_id"] = row[0]
        item["name"] = row[1]
        item["description"] = row[2]
        item["category"] = row[3]
        item["photos"] = row[4]
        item["sellerID"] = row[5]
        item["price"] = row[6]
        item["isFlagged"] = row[7]
        item["watchlist"] = row[8]

        all_items.append(item)
    file.close()
    

    collection.insert_many(all_items)

def view_flagged_items(limit, collection = items_collection):
    """
    This returns all the flagged items
    """
    query = {"isFlagged": "True"}
    results = list(collection.find(query))
    if limit:
        return results[:limit]
    else:
        return results

# I question whether we need this if we have the modify function
def edit_categories(item_id, updated_categories, collection = items_collection):
    query = { "_id" : item_id }
    new_categories = { "$set": { "category": updated_categories } }
    collection.update_one(query, new_categories)

def add_item(id, name, description, category, photos, 
                sellerID, price, isFlagged, watchlist,
                collection = items_collection):
    """
    This adds one item to our database
    """
    item = {"_id": None, "name": None, "description": None,
                "category": None, "photos": None, "sellerID": None,
                "price": None, "isFlagged": None}
    item["_id"] = id
    item["name"] = name
    item["description"] = description
    item["category"] = category
    item["photos"] = photos
    item["sellerID"] = sellerID
    item["price"] = price
    item["isFlagged"] = isFlagged
    item["watchlist"] = watchlist
    collection.insert_one(item)

def ModifyItems(id, name = None, description = None,
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
    for modification in modifications:
        collection.update_one(query, modification)

def get_item(id, collection = items_collection):
    """
    given an item id, this function returns back the item
    """
    query = {"_id": id}
    results = list(collection.find(query))
    return results

def report_item(id, flag_reason, collection = items_collection):
    query = {"_id": id}
    flag = {"$set" : {"isFlagged" : "True" }, "$addtoset": {}}

