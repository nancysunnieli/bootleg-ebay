import pymongo
from pymongo import MongoClient
import csv

client = pymongo.MongoClient("mongodb://root:bootleg@localhost:27019")
db = client["auctions"]
auctions_collection = db["auctions"]
bids_collection = db["bids"]

def create_auctions_collection(data_file_path, 
                                collection = auctions_collection):
    """
    Uploads mock data for auctions into Mongodb database.

    Schema: id, auctionstarttime, auctionendtime, 
            itemid, isBuyNowEnabled, sellerID
    """
    file = open(data_file_path)
    csvreader = csv.reader(file)
    all_entries = []
    for row in csvreader:
        auction = {"_id": None, "auctionstarttime": None,
                "auctionendtime": None, "itemid": None, 
                "isBuyNowEnabled": None, "sellerID": None}
        auction["_id"] = row[0]
        auction["auctionstarttime"] = int(row[1])
        auction["auctionendtime"] = int(row[2])
        auction["itemid"] = row[3]
        auction["isBuyNowEnabled"] = row[4]
        auction["sellerID"] = row[5]
        
        all_entries.append(auction)
    file.close()
    collection.insert_many(all_entries)

def create_bids_collection(data_file_path, 
                            collection = bids_collection):
    """
    Uploads mock data for bids into Mongodb database.

    schema: id, AuctionID, timestamp, amount, userID
    """
    file = open(data_file_path)
    csvreader = csv.reader(file)
    all_entries = []
    for row in csvreader:
        bid = {"_id": None, "AuctionID": None,
                "timestamp": None, "amount": None, 
                "userID": None}
        bid["_id"] = row[0]
        bid["AuctionID"] = row[1]
        bid["timestamp"] = int(row[2])
        bid["amount"] = float(row[3])
        bid["userID"] = row[4]
        
        all_entries.append(bid)
    file.close()
    collection.insert_many(all_entries)


if __name__ == '__main__':
    create_auctions_collection("../../data/mock_data/auctions.csv")
    create_bids_collection("../../data/mock_data/bids.csv")