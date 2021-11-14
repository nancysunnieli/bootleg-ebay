class Cart(object):
    """
    Class for a shopping cart.
    A shopping cart has a User_id
    that it belongs to, as well a list of
    item_ids that are in the cart.
    """
    def __init__(self, user_id = None, items = None):
        self._user_id = user_id
        if items:
            self._items = items
        else:
            self._items = []

    @property
    def user_id(self):
        return self._user_id
    
    @property
    def items(self):
        return self._items

    def from_mongo(self, cart):
        self._user_id = cart["user_id"]
        self.items = cart["items"]
    
    def to_mongo(self):
        return {"user_id": self.user_id, 
                "items": self.items}
    
    def add_item(self, new_item):
        if new_item not in self.items:
            self._items.append(new_item)
            return "ITEM SUCCESSFULLY ADDED"
        else:
            return "ITEM WAS ALREADY IN CART."
    
    def remove_item(self, item):
        if item not in self.items:
            raise "ITEM WAS NOT ALREADY IN CART."
        else:
            self._items.remove(item)
            return "ITEM SUCCESSFULLY REMOVED."
    
    def get_items(self, item):
        return self.items
    
    def empty_cart(self):
        self._items = []


