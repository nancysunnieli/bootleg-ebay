import pymongo
from pymongo import MongoClient
import csv
from bson.objectid import ObjectId

client = pymongo.MongoClient("mongodb://root:bootleg@localhost:27019")
db = client["auctions"]
auctions_collection = db["auctions"]
bids_collection = db["bids"]

def create_auctions_collection(auctions_data_file_path, bids_data_file_path,
                                collection = auctions_collection):
    """
    Uploads mock data for auctions into Mongodb database.

    Schema: id, auctionstarttime, auctionendtime, 
            itemid, isBuyNowEnabled, sellerID
    """
    # getting bids info
    file = open(bids_data_file_path)
    csvreader = csv.reader(file)
    all_bids = []
    for row in csvreader:
        bid = {}
        bid["bid_id"] = ObjectId(row[0])
        bid["AuctionID"] = row[1]
        bid["bid_time"] = int(row[2])
        bid["price"] = float(row[3])
        bid["buyer_id"] = row[4]
        
        all_bids.append(bid)
    file.close()


    file = open(auctions_data_file_path)
    csvreader = csv.reader(file)
    all_entries = []
    for row in csvreader:
        auction = {}
        auction["_id"] = ObjectId(row[0])
        auction["start_time"] = int(row[1])
        auction["end_time"] = int(row[2])
        auction["item_id"] = row[3]
        #auction["buy_now"] = row[4]
        auction["seller_id"] = row[5]
        auction["bids"] = []
        for bid in all_bids:
            if "AuctionID" in bid:
                if bid["AuctionID"] == auction["_id"]:
                    del bid["AuctionID"]
                    auction["bids"].append(bid)

        all_entries.append(auction)
    file.close()
    collection.insert_many(all_entries)



if __name__ == '__main__':
    create_auctions_collection("../../data/mock_data/auctions.csv", "../../data/mock_data/bids.csv")