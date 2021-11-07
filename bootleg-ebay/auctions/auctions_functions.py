import os
import uuid
import datetime
from typing import Sequence
import json

import pymongo

from auction import Auction, Bid, current_time, BadInputError


class AuctionDBManager:

    @classmethod
    def _init_auction_collection(cls):
        hostname = os.getenv('AUCTIONSDBHOST', "localhost")
        port = os.getenv('AUCTIONSDBPORT', "27019")
        client = pymongo.MongoClient(f"mongodb://root:bootleg@{hostname}:{port}")
        db = client["auctions"]
        return db["auctions"]

    @classmethod
    def query_collection(cls, query):
        collection = cls._init_auction_collection()
        results = list(collection.find(query))
        return results

    @classmethod
    def insert_one(cls, dict_):
        collection = cls._init_auction_collection()
        return collection.insert_one(dict_)


    @classmethod
    def delete_one(cls, query):
        collection = cls._init_auction_collection()
        collection.delete_one(query)

    @classmethod
    def delete_many(cls, query):
        collection = cls._init_auction_collection()
        collection.delete_many(query)

    @classmethod
    def update_one(cls, query, values):
        collection = cls._init_auction_collection()
        collection.replace_one(query, values)

    @classmethod
    def get_auction(cls, auction_id) -> Auction:
        """Get an auction by id
        """
        query = {"_id": auction_id}
        result = cls.query_collection(query)[0]
        auction = Auction.from_mongodb_fmt(result)
        return auction

    @classmethod
    def update_auction(cls, auction: Auction) -> None:
        """Update an auction that already exists
        """

        values = auction.to_mongodb_fmt()
        query = { "_id": auction.auction_id}
        cls.update_one(query, values)

def get_auction(auction_id):
    """
    Get an auction. Can either be completed or currently running

    This is used in place of `examineAuctionMetrics()`
    """

    query = {'_id': auction_id}
    auctions = AuctionDBManager.query_collection(query)
    return json.dumps(auctions)

def create_auction(auction_info):
    """
    Create an auction
    """

    auction_id = AuctionDBManager.insert_one(auction_info).inserted_id
    
    if len(AuctionDBManager.query_collection({"_id": auction_id})) > 0:
        auction = AuctionDBManager.get_auction(auction_id)
        auction_json = auction.to_json()
        return auction_json
    else:
        raise BadInputError('We could not create an auction.')


def view_current_auctions() -> Sequence:
    """
    Get the auctions that are currently running.
    """
    
    time = current_time()
    query = {"start_time": {"$lte": time}, 
            "end_time": {"$gte": time}}

    auctions = AuctionDBManager.query_collection(query)
    return json.dumps(auctions)

def remove_auction(auction_id) -> None:
    """
    This removes the auction that matches the auction id.
    This is used when the auction itself
    is force deleted by the admin if it violates conditions.
    """
    query = {"_id" : auction_id}
    AuctionDBManager.delete_one(query)
    if len(AuctionDBManager.query_collection({"_id": auction_id})) == 0:
        return "Auction Successfully deleted!"
    else:
        return "Auction was unable to be successfully deleted."


def bids_by_user(buyer_id):
    """
    This returns back a list of bids by user
    """
    all_auctions = AuctionDBManager.query_collection({})
    all_bids = []
    for current_auction in all_auctions:
        auction = AuctionDBManager.get_auction(current_auction["_id"])
        bids = auction.view_bids(buyer_id=buyer_id)
        all_bids += [b.to_mongodb_fmt() for b in bids]
    return json.dumps(all_bids)

def create_bid(auction_id, price, user_id):
    """
    This is the function that allows users to place
    bids in auctions
    """

    auction = AuctionDBManager.get_auction(auction_id)
    successful = auction.place_bid(price=price, buyer_id=user_id)
    if successful:
        AuctionDBManager.update_auction(auction=auction)
        return "SUCCESSFULLY CREATED BID"
    return "WAS UNABLE TO CREATE BID. PLEASE TRY AGAIN."

def view_bids(auction_id):
    """
    This allows us to view all the bids for a single auction
    """
    auction = AuctionDBManager.get_auction(auction_id)

    bids = auction.view_bids(buyer_id=None)
    bids = [b.to_mongodb_fmt() for b in bids]
    return json.dumps(bids)
    


if __name__ == "__main__":
    """
    print(create_auction({
    "_id": 'dd965614-cb9',
    "seller_id": '63fb9967-8cb',
    "start_time": 1637412397,
    "end_time": 1638556220,
    "item_id": '5878ea47-d84',
    "bids": [
        {
            "bid_id": '16de12f0-7e4',
            "bid_time": 1638422695,
            "price": 41.21,
            "buyer_id": 'f6961483-134'
        }
    ]
    }))
    """
    #print(bids_by_user('db6ef937-1e3'))
    #print(view_current_auctions())
    #print(get_auction('dd965614-cb9'))
    #print(remove_auction('dd965614-cb9'))
    #print(view_bids('dd965614-cb9'))
    #print(create_bid('2f459c3c-c35', 101.99, 'db6ef937-1e3'))


