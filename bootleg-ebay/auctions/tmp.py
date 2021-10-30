
class Item:
    def __init__(self, **kwargs):
        pass

class ItemsManager:
    def __init__(self):
        self.hostname = socket.gethostbyname(socket.gethostname())
        self.client = pymongo.MongoClient("mongodb://root:bootleg@" + self.hostname + ":27017")
        self.db = self.client["items"]
        self.items_collection = self.db["items"]
        self.flagged_items_collection = self.db["flagged_items"]
        self.photos_collection = self.db["photos"]


    def ViewFlaggedItems(self, limit = None, collection = items_collection):
        """
        This returns all the flagged items
        """
        query = {"isFlagged": "True"}

        results = list(collection.find(query))

        # deserialize and instantiate item classes.  
        items = [Item(r) for r in results]

        # perform some manipulation
        # In this case, since the manipulation is rather simple, we don't need to deserialize and reserialize
        # But in more complex operations, creating Item classes can abstract things away and makes things easier to manage
        if limit:
            items = items[:limit]

        # serialize and return out
        return self.ItemsToOutputFormat(items)

    def ItemsToOutputFormat(self, items):
        return [json.dumps(i) for i in items]