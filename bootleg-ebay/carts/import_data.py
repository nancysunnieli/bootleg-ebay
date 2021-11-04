import pymongo
from pymongo import MongoClient
import csv

client = pymongo.MongoClient("mongodb://root:bootleg@localhost:27020")
db = client["carts"]
carts_collection = db["carts"]

def create_carts_collection(carts_data_file_path,
                                collection = carts_collection):
    """
    this creates carts
    """
    
    file = open(carts_data_file_path)
    csvreader = csv.reader(file)
    all_entries = []
    for row in csvreader:
        cart = {}
        cart["_id"] = row[0]
        cart["user_id"] = row[1]
        cart["items"] = []

        all_entries.append(cart)
    file.close()
    collection.insert_many(all_entries)

if __name__ == '__main__':
    create_carts_collection("../../data/mock_data/carts.csv")