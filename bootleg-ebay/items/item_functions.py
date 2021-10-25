import pymongo
from pymongo import MongoClient
import csv


client = pymongo.MongoClient("mongodb://root:bootleg@localhost:27017")
db = client["items"]
items_collection = db["items"]

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

def edit_categories(item_id, updated_categories, collection = items_collection):
    query = { "_id" : item_id }
    new_categories = { "$set": { "category": updated_categories } }
    collection.update_one(query, new_categories)




