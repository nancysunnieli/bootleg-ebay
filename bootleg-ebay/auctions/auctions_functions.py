import pymongo
from pymongo import MongoClient
import uuid
import datetime

client = pymongo.MongoClient("mongodb://root:bootleg@localhost:27019")
db = client["auctions"]
auctions_collection = db["auctions"]
bids_collection = db["bids"]

def generate_random_id():
    return str(uuid.uuid4())[:12]

def ViewAuctions(collection = auctions_collection):
    """
    this gets all the auctions
    that are running at the current time.
    """
    current_time = float(datetime.datetime.now().timestamp())
    query = {"auctionstarttime": {"$lte": current_time }, 
            "auctionendtime": {"$gte": current_time}}
    results = list(collection.find(query))
    return results

def removeAuction(auction_id, 
                    auction_collection = auctions_collection):
    """
    This removes the auction that matches the auction id.
    This is used when an auction is completed, or the auction itself
    is force deleted by the admin if it violates conditions.
    """
    query = {"_id" : auction_id}
    auction_collection.delete_one(query)
    query = {"AuctionID": auction_id}
    auction_collection.delete_many(query)

def AddWinnerCart(auction_id, 
                    auction_collection = auctions_collection,
                    bid_collection = bids_collection):
    """
    This is called when the auction completes,
    and it adds the item to the winner's cart
    """
    query = {"AuctionID" : auction_id }
    results = list(bids_collection.find(query).sort("timestamp",-1).limit(1))

    # results contains the dictionary for the bid that won the auction
    # if results is not empty,
    # I have to call the shopping cart microservice here to add the item
    # to the winner's shopping cart
    # The shopping cart microservice will then call the items microservice
    # to disable the buy now functionality

def CompleteAuction(auction_id, 
                    auction_collection = auctions_collection):
    """
    When the auction completes, we add the item to the winner's
    cart. If there were bids, then we add the item to the winner's cart,
    and while they wait to check out, we will disable the buy now functionality.
    If there were no bids, then we just end the auction, and keep the buy now
    functionality enabled, and do not add the item to anyone's cart,
    In either case, we can delete the auction, since it has been completed.
    We also delete the bids associated with the auction.
    """
    AddWinnerCart(auction_id)
    removeAuction(auction_id)

def BidsByUser(user_id, collection = bids_collection):
    """
    This returns back a list of bids by user
    """
    query = {"userID": user_id}
    results = list(collection.find(query))
    return results

def createBid(AuctionID, amount, userID,
                collection = bids_collection):
    """
    This is the function that allows users to place
    bids in auctions
    """
    bid_id = generate_random_id()
    timestamp = float(datetime.datetime.now().timestamp())
    bid = {"_id": bid_id, "AuctionID": AuctionID, 
            "timestamp": timestamp,
            "amount": amount, "userID": userID}
    result = collection.insert_one(bid)

    if len(list(collection.find({ "_id": bid_id}))) == 1:
            return "Bid Successfully Placed!"
    else:
        return "Bid Was Not Successfully Placed. Please Try Again."

def ViewBids(AuctionID, collection = bids_collection):
    """
    This allows us to view all the bids for a single auction
    """
    query = {"AuctionID": AuctionID}
    results = list(collection.find(query).sort("timestamp",1))
    return results


    


if __name__ == "__main__":
    print(ViewAuctions())
    print(AddWinnerCart('6c3d2078-c47'))



