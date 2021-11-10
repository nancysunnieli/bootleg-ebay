import json
from bson.objectid import ObjectId

class Item(object):
    """
    Class for Item

    Inputs:
        id (string)
        name (string)
        description (string)
        category (array of strings)
        photos (array of strings)
        sellerID (string)
        price (float)
        isFlagged (boolean)
        FlaggedReason (array of strings; 'counterfeit' or 'inappropriate')
        watchlist (array of strings of user_ids)
    """

    def __init__(self, name = None, description = None, category = None, 
                photos = None, sellerID = None, price = None, isFlagged = None, 
                FlaggedReason = None, watchlist = None, quantity = None, shipping = None, id = None):
        self._quantity = quantity
        self._name = name
        self._description = description
        self._category = category
        self._photos = photos
        self._sellerID = sellerID
        self._price = price
        self._isFlagged = isFlagged
        self._id = id
        self._shipping = shipping
        if FlaggedReason == None:
            self._FlaggedReason = []
        else:
            self._FlaggedReason = FlaggedReason
        if watchlist == None:
            self._watchlist = []
        else:
            self._watchlist = watchlist

    

    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @property
    def description(self):
        return self._description
    
    @property
    def category(self):
        return self._category
    
    @property
    def photos(self):
        return self._photos

    @property
    def sellerID(self):
        return self._sellerID
    
    @property
    def price(self):
        return self._price
    
    @property
    def isFlagged(self):
        return self._isFlagged
    
    @property
    def Flagged_Reason(self):
        return self._FlaggedReason

    @property
    def watchlist(self):
        return self._watchlist

    @property
    def quantity(self):
        return self._quantity

    @property
    def shipping(self):
        return self._shipping
    
    def from_mongo(self, item, flagged_info, photo):
        if item == []:
            return
        self._name = item["name"]
        self._description = item["description"]
        self._category = item["category"]
        self._photos = photo
        self._sellerID = item["sellerID"]
        self._price = item["price"]
        self._isFlagged = item["isFlagged"]
        if tuple(item["watchlist"]) == tuple(["True"]):
            self._watchlist = []
        else:
            self._watchlist = item["watchlist"]
        self._quantity = item["quantity"]
        self._shipping = item["shipping"]
        self._FlaggedReason = []
        if self._isFlagged:
            for info in flagged_info:
                self._FlaggedReason.append(info["FlagReason"])
        self._id = item["_id"]

    def to_mongo(self):
        return {"name": self.name, "description": self.description,
                "category": self.category, "photos": self.photos,
                "sellerID": self.sellerID, "price": self.price, "isFlagged": self.isFlagged,
                "watchlist": self.watchlist, "quantity": self.quantity, "shipping": self.shipping}

    def modify_item(self,
                    new_name = None,
                    new_description = None,
                    new_photos = None,
                    new_price = None,
                    new_categories = None,
                    new_watchlist = None,
                    quantity = None,
                    shipping = None):
        """
        This modifies the specified attributes.
        The attributes that can be modified by this
        item are name, description, photos, price,
        and categories
        """
        if new_name:
            self._name = new_name
        if new_description:
            self._description = new_description
        if new_photos:
            self._photos = new_photos
        if new_price:
            self._price = new_price
        if new_categories:
            self._category = new_categories
        if new_watchlist:
            self._watchlist = new_watchlist
        if quantity:
            self._quantity = quantity
        if shipping:
            self._shipping = shipping
    
    def edit_categories(self, new_categories):
        self._category = new_categories
    
    def report_item(self, new_flag_reason):
        if not self.isFlagged:
            self._isFlagged = True
        self._FlaggedReason.append(new_flag_reason)

    def edit_quantity(self):
        if self.quantity == 0:
            return "Item is sold out."
        self._quantity -= 1
        return "Successfully Put Lock On Item."
    
    def add_user_to_watchlist(self, user):
        self._watchlist.append(user)

    def matches_search(self, keywords, category):
        """
        Returns back True if it matches the search.
        Returns back False if it does not.
        """
        if keywords and category:
            matches = False
            for word in keywords:
                if word in self.name or word in self.description:
                    matches = True
                    break
            if category not in self.category:
                matches = False
            return matches
        elif keywords:
            matches = False
            for word in keywords:
                if word in self.name or word in self.description:
                    matches = True
                    break
            return matches
        elif category:
            if category not in self.category:
                return False
            return True


def create_item(name, description, category, photos, 
                sellerID, price, isFlagged, FlaggedReasons, 
                Watchlist, Quantity,
                Id):
    """
    This creates a new item of the item class and
    returns it
    """
    new_item = Item(name, description, category, photos, sellerID, 
                    price, isFlagged, FlaggedReasons, Watchlist, Quantity, Id)
    return new_item


