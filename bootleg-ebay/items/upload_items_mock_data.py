import pymongo
from pymongo import MongoClient
import csv
import re

client = pymongo.MongoClient("mongodb://root:bootleg@localhost:27017")
db = client["items"]
items_collection = db["items"]
flagged_items_collection = db["flagged_items"]
photos_collection = db["photos"]

def reformat_list_csv(array):
    """
    CSV format messes up arrays, so I have to reformat it
    """
    result = array.split(",")
    for i in range(0, len(result)):
        result[i] = re.sub("[\[\]]", "", result[i])
        result[i] = result[i].replace("'", "")
    return result

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
        item["category"] = reformat_list_csv(row[3])
        item["photos"] = row[4]
        item["sellerID"] = row[5]
        item["price"] = row[6]
        item["isFlagged"] = row[7]
        watchlist = reformat_list_csv(row[8])
        item["watchlist"] = watchlist

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


if __name__ == '__main__':
    
    # This is the command to run to create the database in mongo db
    create_all_databases("../../data/mock_data/items.csv", 
                        "../../data/mock_data/flagged_items.csv",
                        "../../data/mock_data/photos.csv")