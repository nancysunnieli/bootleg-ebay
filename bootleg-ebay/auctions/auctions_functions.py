import os
import uuid
import datetime
from typing import Sequence

import pymongo
from pymongo import MongoClient

from auction import Auction, Bid, current_time

"""
Jin- We won't be using AuctionID because mongodb already gives us an id

We'll have one auction collection

Auction should look something like: 
{
    '_id': 12
    'item_id': 10,

    'buy_now': True, # Bool
    'start_time': None, # DateTime
    'end_time': None, # DateTime

    'started': False,
    'completed': False, # Bool

    # The maximum price that is allowed to be bid for this auction. If none, then there's no max
    'max_auction_price': None, # float
    # The max end time set by the seller. 'end_time' can be less than 'max_end_time' if the auction finishes early
    'max_end_time': None, # DateTime

    # The latest bid price and time
    'latest_bid_price': 0.0, # float
    'latest_bid_time': None # Datetime

    'bids': [bid1, bid2, ...]
}

Bid should look like:
{
    '_id': 1
    'price': 99.1
    'buyer_id': 21
    'bid_time': None #Datetime
}
"""

class AuctionDBManager:

    @classmethod
    def _init_auction_collection(cls):
        hostname = os.getenv('AUCTIONSDBHOST', "localhost")
        port = os.getenv('AUCTIONSDBPORT', "27019")
        print(hostname, port)
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
        collection.update_one(query, values)

    @classmethod
    def get_auction(cls, auction_id) -> Auction:
        """Get an auction by id
        """
        query = {"_id": auction_id}
        result = cls.query_collection(query)
        auction = Auction.from_mongodb_fmt(result)
        return auction

    @classmethod
    def update_auction(cls, auction: Auction) -> None:
        """Update an auction that already exists
        """

        values = auction.to_mongodb_fmt()
        query = { "_id": auction.auction_id}
        cls.update_one(query, values)

def CreateAuction(auction_info):
    """Create an auction and start it
    """

    auction_id = AuctionDBManager.insert_one(auction_info).inserted_id
    auction = AuctionDBManager.get_auction(auction_id)
    auction.start_auction()
    AuctionDBManager.update_auction(auction=auction)



def GetAuction(auction_id):
    """Get an auction. Can either be completed or currently running

    This is used in place of `examineAuctionMetrics()`
    """

    query = {'_id': auction_id}
    auctions = AuctionDBManager.query_collection(query)
    return auctions

def ViewCurrentAuctions() -> Sequence:
    """Get the auctions that are currently running.
    """
    
    time = current_time()
    query = {"start_time": {"$lte": time }, 
            "end_time": {"$gte": time}}

    auctions = AuctionDBManager.query_collection(query)
    return auctions

def RemoveAuction(auction_id) -> None:
    """
    This removes the auction that matches the auction id.
    This is used when  the auction itself
    is force deleted by the admin if it violates conditions.
    """
    query = {"_id" : auction_id}
    AuctionDBManager.delete_one(query)

def AddWinnerCart(auction_id):
    """
    This is called when the auction completes,
    and it adds the item to the winner's cart

    # Jin- This should not call the shopping microservice because the point of the mediator is
    to prevent each microservice from talking to each other. We somehow need to do this on 
    the mediator side.
    """

    raise NotImplementedError
    query = {"AuctionID" : auction_id }
    results = list(bids_collection.find(query).sort("timestamp",-1).limit(1))

    # results contains the dictionary for the bid that won the auction
    # if results is not empty,
    # I have to call the shopping cart microservice here to add the item
    # to the winner's shopping cart
    # The shopping cart microservice will then call the items microservice
    # to disable the buy now functionality

def CompleteAuction(auction_id):
    """
    When the auction completes, we add the item to the winner's
    cart. If there were bids, then we add the item to the winner's cart,
    and while they wait to check out, we will disable the buy now functionality.
    If there were no bids, then we just end the auction, and keep the buy now
    functionality enabled, and do not add the item to anyone's cart,
    In either case, we can delete the auction, since it has been completed.
    We also delete the bids associated with the auction.

    # Jin- We shouldn't delete the auction when it's finished. We can just set an attribute "completed" 
    from False to True to indicate that the auction is finished. This is because we may still need the
    auction information later on. For example, a user may want to view finished auctions
    """

    auction = AuctionDBManager.get_auction(auction_id)
    auction.stop_auction()
    AuctionDBManager.update_auction(auction)

def BidsByUser(auction_id, buyer_id):
    """
    This returns back a list of bids by user
    """
    auction = AuctionDBManager.get_auction(auction_id)
    bids = auction.view_bids(buyer_id=buyer_id)
    bids = [b.to_mongodb_fmt() for b in bids]
    return bids

def CreateBid(auction_id, price, user_id):
    """
    This is the function that allows users to place
    bids in auctions
    """

    auction = AuctionDBManager.get_auction(auction_id)
    successful = auction.place_bid(price=price, user_id=user_id)
    if successful:
        AuctionDBManager.update_auction(auction=auction)

    return successful

def ViewBids(auction_id):
    """
    This allows us to view all the bids for a single auction
    """
    auction = AuctionDBManager.get_auction(auction_id)

    bids = auction.view_bids(buyer_id=None)
    bids = [b.to_mongodb_fmt() for b in bids]
    return bids

def BuyNow(auction_id, buyer_id):
    auction = AuctionDBManager.get_auction(auction_id)
    successful = auction.buy_now(buyer_id)

    if successful:
        AuctionDBManager.update_auction(auction=auction)

    return successful


    


if __name__ == "__main__":
    print(ViewCurrentAuctions())
    print(AddWinnerCart('6c3d2078-c47'))



