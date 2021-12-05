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
                photos = None, sellerID = None, isFlagged = None, 
                FlaggedReason = None, watchlist = None, quantity = None, id = None):
        self._quantity = quantity
        self._name = name
        self._description = description
        self._category = category
        self._photos = photos
        self._sellerID = sellerID
        self._isFlagged = isFlagged
        self._id = id
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

    
    def from_mongo(self, item, flagged_info, photo):
        if item == []:
            return
        self._name = item["name"]
        self._description = item["description"]
        self._category = item["category"]
        self._photos = photo
        self._sellerID = item["sellerID"]
        self._isFlagged = item["isFlagged"]
        if tuple(item["watchlist"]) == tuple(["True"]):
            self._watchlist = []
        else:
            self._watchlist = item["watchlist"]
        self._quantity = item["quantity"]
        self._FlaggedReason = []
        if self._isFlagged:
            for info in flagged_info:
                self._FlaggedReason.append(info["FlagReason"])
        self._id = item["_id"]

    def to_mongo(self):
        return {"name": self.name, "description": self.description,
                "category": self.category, "photos": self.photos,
                "sellerID": self.sellerID, "isFlagged": self.isFlagged,
                "watchlist": self.watchlist, "quantity": self.quantity, "_id": self._id}

    def modify_item(self,
                    new_name,
                    new_description,
                    new_photos,
                    new_categories,
                    new_watchlist,
                    quantity):
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
        if new_categories:
            self._category = new_categories
        if new_watchlist:
            self._watchlist = new_watchlist
        if quantity:
            self._quantity = quantity
    
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
    
    def add_user_to_watchlist(self, watchlist_item):
        self._watchlist.append(watchlist_item)

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


