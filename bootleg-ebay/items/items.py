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

    def __init__(self, id, name, description, category, 
                photos, sellerID, price, isFlagged, 
                FlaggedReason, watchlist):
        self._id = id
        self._name = name
        self._description = description
        self._category = category
        self._photos = photos
        self._sellerID = sellerID
        self._price = price
        self._isFlagged = isFlagged
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
    def sellerId(self):
        return self._sellerID
    
    @property
    def price(self):
        return self._price
    
    @property
    def isFlagged(self):
        return self._isFlagged
    
    @property
    def Flagged_Reason(self):
        return self._Flagged_Reason

    @property
    def watchlist(self):
        return self._watchlist
    
    def modifyItem(self,
                    new_name = None,
                    new_description = None,
                    new_photos = None,
                    new_price = None,
                    new_categories = None):
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
    
    def report_item(self, new_flag_reason):
        if not self.isFlagged():
            self._isFlagged = True
        self._Flagged_Reason.append(new_flag_reason)

    def addUserToWatchlist(self, user):
        self._watchlist.append(user)
