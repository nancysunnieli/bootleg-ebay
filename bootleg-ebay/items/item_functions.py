import pymongo
from pymongo import MongoClient
import csv
import uuid
from items import Item


client = pymongo.MongoClient("mongodb://root:bootleg@localhost:27017")
db = client["items"]
items_collection = db["items"]
flagged_items_collection = db["flagged_items"]
photos_collection = db["photos"]


def generate_random_id():
    return str(uuid.uuid4())[:12]

def create_photos_database(data_file_path, collection = photos_collection):
    file = open(data_file_path)
    csvreader = csv.reader(file)
    all_entries = []
    for row in csvreader:
        photo = {"_id": None, "photo": None}
        photo["_id"] = row[0]
        photo["photo"] = row[1]
        all_entries.append(photo)
    file.close()
    collection.insert_many(all_entries)
    
def create_flagged_items_database(data_file_path, collection = flagged_items_collection):
    file = open(data_file_path)
    csvreader = csv.reader(file)
    all_entries = []
    for row in csvreader:
        flagged_item = {"_id": None, "itemID": None, "FlagReason": None}
        flagged_item["_id"] = row[0]
        flagged_item["itemID"] = row[1]
        flagged_item["FlagReason"] = row[2]
        all_entries.append(flagged_item)
    file.close()
    collection.insert_many(all_entries)


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

def create_all_databases(items_data_file_path, flagged_items_data_file_path,
                        photos_data_file_path, item_collection = items_collection, 
                        flagged_item_collection = flagged_items_collection,
                        photo_collection = photos_collection):
    """
    This creates all the collections in our microservice
    """
    create_items_database(items_data_file_path, item_collection)
    create_flagged_items_database(flagged_items_data_file_path, flagged_item_collection)
    create_photos_database(photos_data_file_path, photo_collection)



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

def add_flagged_item(id, item_id, flag_reason, collection = flagged_items_collection):
    """
    This adds a new flag to the database
    """
    item = {"_id": id, "itemID": item_id, "FlaggedReason": flag_reason}
    collection.insert_one(item)

def report_item(id, flag_reason, item_collection = items_collection, 
                flagged_item_collection = flagged_items_collection):
    """
    This flags an item, and gives the flag reason
    """
    # updates item database
    query = {"_id": id}
    flag = {"$set" : {"isFlagged" : "True" }}
    item_collection.update_one(query, flag)

    
    # updates flagged items database
    flag_id = generate_random_id()
    add_flagged_item(flag_id, id, flag_reason)

def RemoveItem():
    pass
