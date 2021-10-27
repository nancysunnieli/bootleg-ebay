from typing import Any, Dict, Optional, Sequence
import datetime

AuctionID = str
UserID = str
DateTime = datetime.date
AuctionInfo = Dict

class Bid:
    """Represents the bid made by a particular user

    """
    def __init__(self, price: float, buyer_id: UserID, bid_time: DateTime) -> None:
        """

        Args:
            price: Bid price
            buyer_id: Id of the buyer making the bid
            bid_time: The time made by the bid
        """
        self._price = price
        self._buyer_id = buyer_id
        self._bid_time = bid_time

    @property
    def price(self):
        return self._price

    @property
    def buyer_id(self):
        return self._buyer_id

    @property
    def bid_time(self):
        return self._bid_time

class Auction:
    """
    
    Args:
        auction_id: Unique id assigned to the auction
        item: Item to be sold. Item Id and seller id should be attached to this
        bids: List of bids made 
        auction_info: Information regarding the auction
    """
    def __init__(
        self, 
        auction_id: AuctionID, 
        # seller_id: UserID, 
        item, 
        bids: Sequence[Bid] = [],
        auction_info: AuctionInfo = {}) -> None:

        self._auction_id = auction_id
        # self._seller_id = seller_id
        self._item = item
        self._bids = bids
        self._auction_info = {
            'buy_now': None, # Bool
            'start_time': None, # Datetime
            'end_time': None, # Datetime

            'started': False,
            'completed': False, # Bool

            # The maximum price that is allowed to be bid for this auction
            'max_auction_price': None, # float

            'current_bid_price': 0.0, # float
            'latest_bid_time': None # Datetime
        }
        self._auction_info.update(auction_info)

        for k, v in self._auction_info.items():
            assert v is not None

    @property
    def auction_id(self):
        return self._auction_id

    # @property
    # def seller_id(self):
    #     return self.seller_id

    @property
    def item(self):
        return self._item

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

        auction_info['start_time'] = datetime.date.today()
        auction_info['started'] = True

    def stop_auction(self) -> None:
        """Stop the auction
        """

        auction_info = self._auction_info
        if auction_info['completed'] is True:
            raise ValueError('You cannot end an auction that already has been completed.')

        auction_info['end_time'] = datetime.date.today()
        auction_info['completed'] = True

    def place_bid(self, bid: Bid) -> None:
        """Place a bid to the auction

        Args:
            bid: A bid made by some user
        """


        auction_info = self._auction_info

        if auction_info['started'] is False:
            raise ValueError('You cannot place a bid on an action that has not been started.')

        if auction_info['completed'] is True:
            raise ValueError('You cannot place a bid on an auction that has been finished.')

        if bid.price > auction_info['current_bid_price'] and bid.bid_time > auction_info['latest_bid_time']:
            self._bids.append(bid)

        # end the auction if the bid price is greater than the maximum auction price
        if bid.price >= auction_info['max_auction_price']:
            self.stop_auction()

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
        
        bid = Bid(
            price=auction_info['max_auction_price'],
            buyer_id=buyer_id,
            bid_time=datetime.date.today())

        self.place_bid(bid)

            

    