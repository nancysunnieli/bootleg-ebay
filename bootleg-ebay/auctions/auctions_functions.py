import os
import uuid
import datetime
from typing import Sequence
import json

import pymongo
from bson.objectid import ObjectId

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
        query = {"_id": ObjectId(auction_id)}
        result = cls.query_collection(query)
        
        if len(result) == 0:
            raise BadInputError('We could not find any auctions with id {}'.format(auction_id))
        result = result[0]
        
        auction = Auction.from_mongodb_fmt(result)
        return auction

    @classmethod
    def update_auction(cls, auction: Auction) -> None:
        """Update an auction that already exists
        """

        values = auction.to_dict()
        del values['auction_id']
        query = { "_id": ObjectId(auction.auction_id)}
        cls.update_one(query, values)

def get_auction(auction_id):
    """
    Get an auction. Can either be completed or currently running

    """

    auctions = AuctionDBManager.get_auction(auction_id)
    return auctions.to_json()

def get_auctions_by_item_id(item_id):
    """Get all the auctions corresponding to an item.
    """

    query = {"item_id": item_id}
    auctions_mongo = AuctionDBManager.query_collection(query)
    
    if len(auctions_mongo) == 0:
        raise BadInputError('We could not find any auctions with item_id {}'.format(item_id))

    auctions = [Auction.from_mongodb_fmt(a) for a in auctions_mongo]
    auctions_json = json.dumps([a.to_dict() for a in auctions])
    return auctions_json  




def create_auction(auction_info):
    """
    Create an auction
    """

    if auction_info['end_time'] <= auction_info['start_time']:
        raise BadInputError('The end time must be greater than the start time.')
        
    auction_id = AuctionDBManager.insert_one(auction_info).inserted_id
    
    if len(AuctionDBManager.query_collection({"_id": auction_id})) > 0:
        auction = AuctionDBManager.get_auction(auction_id)
        auction_json = auction.to_json()
        return auction_json
    else:
        raise BadInputError('We could not create an auction.')




def get_auction_metrics(start, end):
    """Examine the auctions that have been completed
    """
    query = {"start_time": {"$lte": start}, 
            "end_time": {"$gte": end}}

    time = current_time()
    auctions_mongo = AuctionDBManager.query_collection(query)

    auctions = [Auction.from_mongodb_fmt(a) for a in auctions_mongo]

    # get the completed auctions
    auctions = list(filter(lambda x: x.auction_info['end_time'] <= time, auctions))

    if len(auctions) == 0:
        metrics = {
            'average_auction_time': -1,
            'longest_auction_time': -1,
            'shortest_auction_time': -1,
            'mean_price': -1,
            'highest_price': -1,
            'lowest_price': -1
        }
    else:
        auction_times = []
        prices = []
        for a in auctions:
            auction_times.append(a.auction_info['end_time'] - a.auction_info['start_time'])
            prices.append(a.bids[-1].price)

        metrics = {
            'average_auction_time': sum(auction_times) / len(auction_times),
            'longest_auction_time': max(auction_times),
            'shortest_auction_time': min(auction_times),
            'mean_price': sum(prices) / len(prices),
            'highest_price': max(prices),
            'lowest_price': min(prices)
        }

    return json.dumps(metrics)





def view_current_auctions() -> Sequence:
    """
    Get the auctions that are currently running.
    """

    time = current_time()
    query = {"start_time": {"$lte": time}, 
            "end_time": {"$gte": time}}

    auctions_mongo = AuctionDBManager.query_collection(query)
    auctions = [Auction.from_mongodb_fmt(a) for a in auctions_mongo]
    auctions_json = json.dumps([a.to_dict() for a in auctions])
    return auctions_json

def remove_auction(auction_id) -> None:
    """
    This removes the auction that matches the auction id.
    This is used when the auction itself
    is force deleted by the admin if it violates conditions.
    """
    query = {"_id" : ObjectId(auction_id)}
    AuctionDBManager.delete_one(query)
    if len(AuctionDBManager.query_collection({"_id": auction_id})) == 0:
        return json.dumps({})
    else:
        raise BadInputError('We could not delete auction with id {}'.format(auction_id))


def user_bids(buyer_id):
    """
    This returns back a list of bids by user
    """
    all_auctions = AuctionDBManager.query_collection({})
    all_bids = []
    for current_auction in all_auctions:
        auction = AuctionDBManager.get_auction(current_auction["_id"])
        bids = auction.view_bids(buyer_id=buyer_id)
        all_bids += [b.to_dict() for b in bids]
    return json.dumps(all_bids)

def create_bid(auction_id, price, user_id):
    """
    This is the function that allows users to place
    bids in auctions
    """

    auction = AuctionDBManager.get_auction(auction_id)
    auction.place_bid(price=price, buyer_id=user_id)
    AuctionDBManager.update_auction(auction=auction)

    auction = AuctionDBManager.get_auction(auction_id)
    if len(auction.bids) == 0:
        raise ValueError('Bid was placed unsuccessfully')
    bid = auction.bids[-1]
    return bid.to_json()

def view_bids(auction_id):
    """
    This allows us to view all the bids for a single auction
    """
    auction = AuctionDBManager.get_auction(auction_id)

    bids = auction.view_bids(buyer_id=None)
    bids = [b.to_dict() for b in bids]
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
    #print(user_bids('db6ef937-1e3'))
    #print(view_current_auctions())
    #print(get_auction('dd965614-cb9'))
    #print(remove_auction('dd965614-cb9'))
    #print(view_bids('dd965614-cb9'))
    #print(create_bid('2f459c3c-c35', 101.99, 'db6ef937-1e3'))


