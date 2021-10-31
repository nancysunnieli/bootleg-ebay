from typing import Any, Dict, Optional, Sequence
import datetime

AuctionID = int
BidID = Optional[int]
UserID = int
Price = float
DateTime = Optional[float]
AuctionInfo = Dict
MongoDBData = Dict[str, Any]

def current_time():
    return float(datetime.datetime.now().timestamp())

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
            bid_id=mongodb_data['_id'],
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
            bid_info['_id'] = self.bid_id


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
            'buy_now': None, # Bool

            # start time of the auction
            'start_time': None, # DateTime
            # end time of the auction
            'end_time': None, # DateTime

            'started': False,
            'completed': False, # Bool

            # The maximum price that is allowed to be bid for this auction
            'max_auction_price': None, # float
            # The max end time set by the seller. 'end_time' can be less than 'max_end_time' if the auction finishes early
            'max_end_time': None, # DateTime

            'latest_bid_price': -1.0, # float
            'latest_bid_time': None # DateTime
        }

        for k in auction_info.keys():
            if k not in self._auction_info:
                raise ValueError('You cannot have key: {} for `aucton_info`'.format(k))

        self._auction_info.update(auction_info)

        # i.e. if the auction expired
        if current_time() > self._auction_info['max_end_time']:
            self.stop_auction()


        # for k, v in self._auction_info.items():
        #     assert v is not None

    @classmethod
    def from_mongodb_fmt(cls, mongodb_data: MongoDBData):
        """Convert mongodb format data into Bid class

        Args:
            mongodb_data: Data format given by mongodb

        Returns:
            auction (Auction)
        """

        bids = [Bid.from_mongodb_fmt(bid) for bid in mongodb_data['bids']]
        auction_id = mongodb_data['_id']
        del mongodb_data['bids']
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

    @property
    def auction_id(self):
        return self._auction_id

    @property
    def bids(self):
        return self._bids

    @property
    def auction_info(self):
        return self._auction_info

    def start_auction(self) -> None:
        """Start the auction
        """
        
        auction_info = self._auction_info
        if auction_info['start_time'] is not None:
            raise ValueError('You cannot start an auction that has already been started.')

        auction_info['start_time'] = current_time()
        auction_info['started'] = True

    def stop_auction(self) -> None:
        """Stop the auction
        """

        auction_info = self._auction_info
        if auction_info['completed'] is True:
            raise ValueError('You cannot end an auction that already has been completed.')

        auction_info['end_time'] = current_time()
        auction_info['completed'] = True

    def place_bid(self, buyer_id, price) -> bool:
        """Place a bid to the auction

        Args:
            bid: A bid made by some user

        Returns:
            True if a bid was successfully placed. False if otherwise
        """

        bid = Bid(bid_id=None, price=price, buyer_id=buyer_id)
        auction_info = self._auction_info

        if auction_info['started'] is False:
            raise ValueError('You cannot place a bid on an action that has not been started.')

        if auction_info['completed'] is True:
            raise ValueError('You cannot place a bid on an auction that has been finished.')

        if bid.price > auction_info['latest_bid_price'] and bid.bid_time > auction_info['latest_bid_time']:
            self._bids.append(bid)
            successful = True
            auction_info['latest_bid_price'] = bid.price
            auction_info['latest_bid_time'] = bid.bid_time
        else:
            successful = False

        # end the auction if the bid price is greater than the maximum auction price
        if bid.price >= auction_info['max_auction_price']:
            self.stop_auction()

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

    def buy_now(self, buyer_id: UserID) -> None:
        """Buy the item in the auction instaneously
        """

        # This is logically equivalent to placing a bid with the price equal to the maximum auction bid price
        auction_info = self._auction_info 
        
        successful = self.place_bid(buyer_id, auction_info['max_auction_price'])

        return successful

            

    