from typing import Any, Dict, Optional, Sequence
import datetime
import json

AuctionID = str
BidID = Optional[int]
UserID = int
Price = float
DateTime = Optional[float]
AuctionInfo = Dict
MongoDBData = Dict[str, Any]

def current_time():
    return float(datetime.datetime.now().timestamp())

class APIError(Exception):
    """All custom API Exceptions"""
    pass 

class BadInputError(APIError):
    """Custom bad input error class."""
    code = 400
    description = "Bad input Error"

class Bid:
    """Represents the bid made by a particular user

    """
    def __init__(
        self, 
        bid_id: BidID, 
        price: Price, 
        buyer_id: UserID, 
        bid_time: DateTime = None) -> None:
        """

        Args:
            price: Bid price
            buyer_id: Id of the buyer making the bid
            bid_time: The time made by the bid
        """
        
        assert price >= 0

        self._bid_id = bid_id
        self._price = price
        self._buyer_id = buyer_id

        if bid_time is None:
            bid_time = current_time()

        self._bid_time = bid_time

    @property
    def bid_id(self):
        return self._bid_id

    @property
    def price(self):
        return self._price

    @property
    def buyer_id(self):
        return self._buyer_id

    @property
    def bid_time(self):
        return self._bid_time

    @classmethod
    def from_mongodb_fmt(cls, mongodb_data: MongoDBData):
        """Convert mongodb format data into Bid class

        Args:
            mongodb_data: Data format given by mongodb

        Returns:
            bid (Bid)
        """
        bid = cls(
            bid_id=str(mongodb_data['bid_id']),
            price=mongodb_data['price'],
            buyer_id=mongodb_data['buyer_id'],
            bid_time=mongodb_data['bid_time'])

        return bid

    def to_mongodb_fmt(self) -> MongoDBData:
        """Export this class to mongodb format
        """

        bid_info = {
            'price': self.price,
            'buyer_id': self.buyer_id,
            'bid_time': self.bid_time
        }

        if self.bid_id is not None:
            bid_info['bid_id'] = self.bid_id


        return bid_info


class Auction:
    """Represents the auction
    
    """
    def __init__(
        self, 
        auction_id: AuctionID, 
        bids: Sequence[Bid] = [],
        auction_info: AuctionInfo = {}) -> None:
        """
        Args:
            auction_id: Unique id assigned to the auction
            bids: List of bids made 
            auction_info: Information regarding the auction
        """

        self._auction_id = auction_id
        # self._seller_id = seller_id
        self._bids = bids
        self._auction_info = {
            'item_id': None,
            'seller_id': None,
            # start time of the auction
            'start_time': None, # DateTime
            # end time of the auction
            'end_time': None, # DateTime
        }

        for k in auction_info.keys():
            if k not in self._auction_info:
                raise ValueError('You cannot have key:' + k + ' for `auction_info`')

        self._auction_info.update(auction_info)


    @classmethod
    def from_mongodb_fmt(cls, mongodb_data: MongoDBData):
        """Convert mongodb format data into Bid class

        Args:
            mongodb_data: Data format given by mongodb

        Returns:
            auction (Auction)
        """

        if 'bids' in mongodb_data:
            bids = [Bid.from_mongodb_fmt(bid) for bid in mongodb_data['bids']]
            del mongodb_data['bids']
        else:
            bids = []

        auction_id = str(mongodb_data['_id'])
        
        del mongodb_data['_id']
        
        auction = cls(auction_id=auction_id, bids=bids, auction_info=mongodb_data)
        return auction

    def to_mongodb_fmt(self):
        """Export this class to mongodb format
        """
        mongodb_dict = self.auction_info
        mongodb_dict['_id'] = self.auction_id
        mongodb_dict['bids'] = [b.to_mongodb_fmt() for b in self.bids]

        return mongodb_dict

    def to_json(self):
        dict_ = self.to_mongodb_fmt()
        return json.dumps(dict_)

    @property
    def auction_id(self):
        return self._auction_id

    @property
    def bids(self):
        return self._bids

    @property
    def auction_info(self):
        return self._auction_info

    def previous_bid(self):
        highest_price = -1
        latest_bid = -float('inf')
        for bid in self.bids:
            if bid.bid_time > latest_bid:
                if bid.price > highest_price:
                    latest_bid = bid.bid_time
                    highest_price = bid.price
        return highest_price, latest_bid


    def place_bid(self, buyer_id, price) -> bool:
        """Place a bid to the auction

        Args:
            bid: A bid made by some user

        Returns:
            True if a bid was successfully placed. False if otherwise
        """

        bid = Bid(bid_id=None, price=price, buyer_id=buyer_id)
        auction_info = self._auction_info
        
        if auction_info['start_time'] > bid.bid_time:
            raise ValueError('You cannot place a bid on an action that has not started.')

        if auction_info['end_time'] < bid.bid_time:
            raise ValueError('You cannot place a bid on an auction that has finished.')

        
        highest_price, latest_bid = self.previous_bid()

        if bid.price > highest_price and bid.bid_time > latest_bid:
            self._bids.append(bid)
            successful = True
        else:
            successful = False

        return successful

    def view_bids(self, buyer_id: Optional[UserID] = None) -> Sequence[Bid]:
        """View all the bids

        Args:
            buyer_id: If None, then we view all the bids. Otherwise, we view the bids by a particular user
        """

        if buyer_id is None:
            return self.bids
        else:
            return list(filter(lambda x: x.buyer_id == buyer_id, self.bids))

            

    